from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_community.chat_models import ChatOCIGenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_mcp_adapters.tools import load_mcp_tools

server_params = StdioServerParameters(
    command="npx",
    args=["@browsermcp/mcp@latest"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize the connection
        await session.initialize()

        # Get tools
        tools = await load_mcp_tools(session)

        # Create and run the agent
        # Please replace the placeholders with your actual OCI configuration
        llm = ChatOCIGenAI(
            auth_type="API_KEY",  # Set to 'SECURITY_TOKEN', 'INSTANCE_PRINCIPAL', etc. as needed
            compartment_id="YOUR_COMPARTMENT_ID",
            service_endpoint="YOUR_SERVICE_ENDPOINT",  # e.g. https://inference.generativeai.us-chicago-1.oci.oraclecloud.com
            model_id="cohere.command-r-plus",  # or another supported model
            is_stream=True,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        agent_response = await agent_executor.ainvoke({"input": "what's (3 + 5) x 12?"})
        print(agent_response)


