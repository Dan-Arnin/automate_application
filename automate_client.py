import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_community.chat_models import ChatOCIGenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_mcp_adapters.tools import load_mcp_tools

# Import new modules
from prompts import get_system_prompt
from application_tracker import ApplicationTracker, ApplicationStatus
from error_handler import (
    ApplicationError, CaptchaError, AuthenticationError,
    handle_error, is_retryable_error
)
from logger_setup import get_application_logger, get_system_logger
from config import Config

# Import user context
try:
    from user_context import USER_DETAILS
except ImportError:
    print("Error: user_context.py not found. Please create it with your details.")
    exit(1)

# Initialize loggers
app_logger = get_application_logger()
sys_logger = get_system_logger()

async def main():
    sys_logger.info("Starting Job Application Automation System")
    sys_logger.info(f"Configuration: {Config.get_config_summary()}")
    
    # Initialize application tracker
    tracker = ApplicationTracker()
    stats = tracker.get_statistics()
    sys_logger.info(f"Application Statistics: {stats}")
    
    server_params = StdioServerParameters(
        command="npx",
        args=["@browsermcp/mcp@latest"]
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                sys_logger.info("MCP session initialized successfully")

                # Get tools
                tools = await load_mcp_tools(session)
                sys_logger.info(f"Loaded {len(tools)} browser automation tools")

                # Initialize OCI GenAI
                llm = ChatOCIGenAI(
                    auth_type="API_KEY",
                    compartment_id="ocid1.tenancy.oc1..aaaaaaaahqvb2kliqi35z57qalhpr4dyqbjprclszdcoar2wgc7q6nl36aba",
                    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
                    model_id="xai.grok-4-fast-non-reasoning"
                )
                sys_logger.info("LLM initialized successfully")

                # Get system prompt
                system_prompt = get_system_prompt(mode="application")

                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{input}"),
                    ("placeholder", "{agent_scratchpad}"),
                ])

                agent = create_tool_calling_agent(llm, tools, prompt)
                agent_executor = AgentExecutor(
                    agent=agent, 
                    tools=tools, 
                    verbose=True,
                    max_iterations=15,
                    handle_parsing_errors=True
                )
                
                print("\n" + "="*60)
                print("🤖 Job Application Agent Ready!")
                print("="*60)
                print(f"User: {USER_DETAILS['first_name']} {USER_DETAILS['last_name']}")
                print(f"Total Applications: {stats['total']}")
                print(f"Completed: {stats['by_status'].get('completed', 0)}")
                print(f"Failed: {stats['by_status'].get('failed', 0)}")
                print("="*60)
                print("\nCommands:")
                print("  - Paste a job application URL to start applying")
                print("  - Type 'stats' to see application statistics")
                print("  - Type 'export' to export applications to CSV")
                print("  - Type 'exit' or 'quit' to stop")
                print("="*60 + "\n")
                
                current_app_id = None
                
                while True:
                    try:
                        user_input = input("You: ").strip()
                        
                        if not user_input:
                            continue
                        
                        if user_input.lower() in ['exit', 'quit']:
                            print("Saving application history...")
                            tracker.save()
                            print("Goodbye! 👋")
                            break
                        
                        # Handle special commands
                        if user_input.lower() == 'stats':
                            stats = tracker.get_statistics()
                            print("\n📊 Application Statistics:")
                            print(f"  Total: {stats['total']}")
                            for status, count in stats['by_status'].items():
                                print(f"  {status.title()}: {count}")
                            print()
                            continue
                        
                        if user_input.lower() == 'export':
                            export_path = Config.DATA_DIR / "applications_export.csv"
                            tracker.export_to_csv(export_path)
                            print(f"✅ Exported to {export_path}\n")
                            continue
                        
                        # Check if input looks like a job application URL
                        if user_input.startswith('http'):
                            # Check for duplicates
                            if tracker.is_duplicate(user_input):
                                print("⚠️  You've already applied to this job!")
                                existing = tracker.get_application(tracker._generate_app_id(user_input))
                                print(f"   Applied on: {existing['created_at']}")
                                print(f"   Status: {existing['status']}")
                                
                                confirm = input("   Apply again anyway? (yes/no): ").strip().lower()
                                if confirm != 'yes':
                                    continue
                            
                            # Create new application entry
                            print("📝 Creating new application entry...")
                            print("   Company name: ", end="")
                            company = input().strip() or "Unknown Company"
                            print("   Position: ", end="")
                            position = input().strip() or "Unknown Position"
                            
                            current_app_id = tracker.add_application(
                                url=user_input,
                                company=company,
                                position=position,
                                status=ApplicationStatus.IN_PROGRESS
                            )
                            
                            app_logger.info(f"Starting application: {company} - {position}")
                            print(f"🚀 Starting application process...\n")
                        
                        # Execute the agent
                        try:
                            tracker.increment_attempts(current_app_id) if current_app_id else None
                            
                            print("🤖 Agent working...\n")
                            
                            async for chunk in agent_executor.astream({"input": user_input}):
                                if "actions" in chunk:
                                    for action in chunk["actions"]:
                                        print(f"⚙️  Executing: {action.tool}")
                                        app_logger.info(f"Tool: {action.tool}, Input: {action.tool_input}")
                                        
                                elif "steps" in chunk:
                                    for step in chunk["steps"]:
                                        print(f"✅ Completed: {step.action.tool}")
                                        
                                elif "output" in chunk:
                                    print(f"\n🤖 Agent: {chunk['output']}\n")
                                    app_logger.info(f"Agent output: {chunk['output']}")
                            
                            # Mark as completed if we got here without errors
                            if current_app_id:
                                tracker.update_status(current_app_id, ApplicationStatus.COMPLETED)
                                print("✅ Application completed successfully!\n")
                                app_logger.info(f"Application {current_app_id} completed")
                                current_app_id = None
                                
                        except CaptchaError as e:
                            print(f"\n🔒 CAPTCHA detected! Please solve it manually and try again.\n")
                            if current_app_id:
                                tracker.update_status(
                                    current_app_id,
                                    ApplicationStatus.REQUIRES_MANUAL,
                                    handle_error(e, "CAPTCHA encountered")
                                )
                            app_logger.warning(f"CAPTCHA error: {e}")
                            
                        except AuthenticationError as e:
                            print(f"\n🔐 Authentication required! Please log in and try again.\n")
                            if current_app_id:
                                tracker.update_status(
                                    current_app_id,
                                    ApplicationStatus.REQUIRES_MANUAL,
                                    handle_error(e, "Authentication required")
                                )
                            app_logger.warning(f"Authentication error: {e}")
                            
                        except ApplicationError as e:
                            error_info = handle_error(e, "Application process")
                            print(f"\n❌ Application error: {e.message}")
                            
                            if is_retryable_error(e):
                                print("   This error might be temporary. You can try again.\n")
                            else:
                                print("   Manual intervention may be required.\n")
                            
                            if current_app_id:
                                tracker.update_status(
                                    current_app_id,
                                    ApplicationStatus.FAILED,
                                    error_info
                                )
                            app_logger.error(f"Application error: {e}")
                            
                        except Exception as e:
                            error_info = handle_error(e, "Unexpected error")
                            print(f"\n❌ An unexpected error occurred: {str(e)}\n")
                            
                            if current_app_id:
                                tracker.update_status(
                                    current_app_id,
                                    ApplicationStatus.FAILED,
                                    error_info
                                )
                            sys_logger.error(f"Unexpected error: {e}", exc_info=True)
                            
                    except KeyboardInterrupt:
                        print("\n\n⚠️  Interrupted by user")
                        if current_app_id:
                            tracker.update_status(current_app_id, ApplicationStatus.FAILED)
                        tracker.save()
                        break
                    
                    except Exception as e:
                        sys_logger.error(f"Error in main loop: {e}", exc_info=True)
                        print(f"❌ Error: {str(e)}\n")
                        continue
    
    except Exception as e:
        sys_logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"❌ Fatal error: {str(e)}")
        print("Please check the logs for more details.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)

