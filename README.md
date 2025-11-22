# Job Application Automation System

An intelligent, robust job application automation system using Browser MCP and LangChain with OCI GenAI.

## Features

✅ **Automated Job Applications** - Fill out job application forms automatically  
✅ **Multi-Platform Support** - Works with Greenhouse, Lever, Workday, LinkedIn, and more  
✅ **Smart Form Detection** - Intelligently maps form fields to your data  
✅ **Application Tracking** - Tracks all applications with status and history  
✅ **Error Handling** - Robust retry logic and error recovery  
✅ **Duplicate Prevention** - Prevents applying to the same job twice  
✅ **Structured Logging** - Detailed logs for debugging and monitoring  
✅ **Export Capabilities** - Export application history to CSV  

## Prerequisites

- Node.js (for Browser MCP)
- Python 3.8+
- Chrome browser with Browser MCP extension installed
- OCI account with GenAI access

## Installation

1. **Install Browser MCP Extension**
   - Follow instructions at https://docs.browsermcp.io/setup-extension

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure User Details**
   - Edit `user_context.py` and fill in your personal information
   - Update resume path, contact details, work experience, etc.

4. **Configure OCI Credentials**
   - Ensure your OCI API key is configured
   - Update compartment ID in `automate_client.py` if needed

## Usage

### Starting the Agent

```bash
python automate_client.py
```

### Commands

Once the agent is running, you can use these commands:

- **Apply to a job**: Paste the job application URL
- **View statistics**: Type `stats`
- **Export applications**: Type `export`
- **Exit**: Type `exit` or `quit`

### Example Workflow

1. Start the agent:
   ```bash
   python automate_client.py
   ```

2. Paste a job application URL:
   ```
   You: https://boards.greenhouse.io/company/jobs/123456
   ```

3. Enter company and position when prompted:
   ```
   Company name: Google
   Position: Software Engineer
   ```

4. The agent will:
   - Navigate to the application page
   - Fill in your information
   - Upload your resume
   - Answer screening questions
   - Ask for confirmation before submitting

## Project Structure

```
Automate-application-mcp/
├── automate_client.py          # Main application entry point
├── user_context.py              # Your personal information
├── prompts.py                   # System prompts for the AI agent
├── application_tracker.py       # Application state tracking
├── error_handler.py             # Error handling and retry logic
├── config.py                    # Configuration settings
├── logger_setup.py              # Logging configuration
├── logs/                        # Log files
│   ├── applications.log         # Application events
│   └── system.log               # System events
├── data/                        # Application data
│   └── applications.json        # Application history
└── requirements.txt             # Python dependencies
```

## Configuration

Edit `config.py` to customize:

- **Retry Settings**: Max attempts, backoff multiplier
- **Timeouts**: Page load, element wait times
- **Logging**: Log levels, file rotation
- **Application Settings**: Duplicate prevention, auto-save

## Application Tracking

All applications are tracked in `data/applications.json` with:

- Application URL
- Company and position
- Status (pending, in_progress, completed, failed, requires_manual)
- Timestamps
- Error history
- Number of attempts

### Application Statuses

- **pending**: Not yet started
- **in_progress**: Currently being filled out
- **completed**: Successfully submitted
- **failed**: Failed with errors
- **requires_manual**: Needs manual intervention (CAPTCHA, authentication)

## Error Handling

The system handles various error scenarios:

- **Network Errors**: Automatic retry with exponential backoff
- **CAPTCHA**: Notifies user for manual intervention
- **Authentication**: Prompts user to log in
- **Form Validation**: Asks user for missing information
- **Timeouts**: Retries with longer wait times

## Logs

Two log files are maintained:

- `logs/applications.log`: Application-specific events (form fills, submissions)
- `logs/system.log`: System events (initialization, errors, debugging)

Logs rotate automatically when they reach 10MB, keeping 5 backup files.

## Tips for Best Results

1. **Keep Browser Open**: Make sure Chrome is running with the Browser MCP extension
2. **Stay Logged In**: Log into job platforms beforehand (LinkedIn, Greenhouse, etc.)
3. **Review Before Submit**: Always review the agent's work before confirming submission
4. **Update User Context**: Keep your information current in `user_context.py`
5. **Check Logs**: If something goes wrong, check the logs for details

## Common Issues

### "CAPTCHA detected"
- Solve the CAPTCHA manually in the browser
- Type the same command again to retry

### "Authentication required"
- Log into the platform manually in the browser
- The agent will continue once you're logged in

### "Element not found"
- The page might be loading slowly
- The agent will retry automatically
- If it persists, the site structure might be unusual

### "Duplicate application"
- You've already applied to this job
- Check `data/applications.json` for history
- Type `yes` when prompted to apply again anyway

## Exporting Data

Export your application history to CSV:

```
You: export
```

This creates `data/applications_export.csv` with all your applications.

## Security & Privacy

- All data stays local on your machine
- Resume and personal information are never sent to external servers (except the job application sites)
- Logs don't contain sensitive information like passwords
- Application history is stored locally in `data/applications.json`

## Troubleshooting

1. **Check logs**: `logs/system.log` and `logs/applications.log`
2. **Verify user context**: Ensure `user_context.py` is filled out correctly
3. **Test browser connection**: Make sure Browser MCP extension is active
4. **Check OCI credentials**: Verify your OCI API key is valid

## Support

For issues or questions:
- Check the logs in `logs/` directory
- Review the Browser MCP documentation: https://docs.browsermcp.io
- Verify your user context is properly configured

## License

This project is for personal use in job searching automation.
