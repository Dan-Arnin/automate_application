# User Context for Job Application Automation

# PLEASE FILL IN YOUR DETAILS BELOW
USER_DETAILS = {
    # Basic Information
    "first_name": "Dharshan",
    "last_name": "A.N.",
    "email": "andharshan@gmail.com",
    "phone": "+91 9483937849",
    
    # Professional Links
    "linkedin_url": "https://linkedin.com/in/dharshan-a-n-75b9a720b",
    "portfolio_url": "",  # Optional
    "github_url": "https://github.com/Dan-Arnin",
    "website_url": "",  # Optional
    
    # Location
    "location": "Bangalore, Karnataka, India",
    "willing_to_relocate": True,
    "requires_sponsorship": False,  # Adjust based on target country
    
    # Resume/Documents
    # IMPORTANT: Use absolute path to your resume file
    "resume_path": r"i:\Dan dev\Codes\Automate-application-mcp\Dharshan A.N. resume.pdf",
    "cover_letter_path": "",  # Optional: path to cover letter template
    
    # Professional Summary
    "experience_summary": """
    I am an AI/ML Engineer with 1+ year of professional experience specializing in Generative AI, 
    RAG systems, and enterprise AI solutions. I have led the design and implementation of AI solutions 
    leveraging Oracle Cloud Infrastructure (OCI) and AWS, building advanced RAG systems, Text-to-SQL 
    applications, and multi-agent AI systems. My expertise includes working with state-of-the-art LLMs 
    (GPT-5, Claude 4.5 Sonnet, Llama-4-Maverick, Qwen 2.5) using LangChain, LlamaIndex and Strands frameworks. 
    I am passionate about building scalable AI systems and automating complex enterprise workflows.
    """,
    
    # Years of Experience
    "years_of_experience": 1.5,  # Apr 2024 - Present (L1 AI Consultant) + Oct 2023 - Apr 2024 (ML Intern)
    
    # Education
    "education": [
        {
            "degree": "Bachelor of Engineering - B.E., AI and ML",
            "university": "New Horizon College of Engineering",
            "graduation_year": "2024",
            "gpa": "9.54/10",
            "location": "Bangalore, India",
            "duration": "2020 - 2024"
        }
    ],
    
    # Work Experience (most recent first)
    "work_experience": [
        {
            "title": "L1 AI Consultant",
            "company": "Conneqtion Consulting Group",
            "duration": "Apr 2024 - Present",
            "location": "Bangalore, India",
            "description": """Led design and implementation of Generative AI solutions leveraging Oracle Cloud Infrastructure (OCI) to streamline enterprise workflows. Built advanced Retrieval-Augmented Generation (RAG) systems, improving accuracy and reducing response time by 40%. Enhanced Smart OCR capabilities with cutting-edge models, boosting document efficiency by 30%. Developed Text-to-SQL application with Oracle ADW/ATP and Oracle 23AI DB, reducing query time by 30%. Collaborated with global teams in ERP system deployments across ME and Europe regions to deploy multi-agent AI systems at scale. Utilized state-of-the-art LLMs (GPT-4o, Mistral-Large, Llama 3.x, Mixtral-8x22B) with LangChain & LlamaIndex for automation.""",
            "achievements": [
                "Improved RAG system accuracy and reduced response time by 40%",
                "Boosted document processing efficiency by 30% with Smart OCR",
                "Reduced query time by 30% with Text-to-SQL application",
                "Deployed multi-agent AI systems across ME and Europe regions"
            ]
        },
        {
            "title": "Machine Learning Intern",
            "company": "GaugeAI",
            "duration": "Oct 2023 - Apr 2024",
            "location": "Remote",
            "description": """Designed database architecture in MySQL and Python backend using FastAPI, reducing API response time by 20%. Implemented websockets enabling parallel sessions, enhancing system scalability. Integrated LLMs with Guidance and LangChain frameworks, achieving 30% improvement in conversational accuracy. Built guardrail systems for secure querying, reducing vulnerability incidents by 40%.""",
            "achievements": [
                "Reduced API response time by 20% with optimized FastAPI backend",
                "Improved conversational accuracy by 30% with LLM integration",
                "Reduced security vulnerabilities by 40% with guardrail systems"
            ]
        }
    ],
    
    # Skills (for keyword matching)
    "skills": [
        # Languages
        "Python", "Java", "C", "C++", "C#", "JavaScript", "SQL",
        # AI/ML
        "TensorFlow", "PyTorch", "Scikit-Learn", "LangChain", "LlamaIndex", 
        "RAG Systems", "Generative AI", "LLMs", "NLP", "Machine Learning",
        "GPT-4o", "Mistral", "Llama", "Mixtral",
        # Cloud
        "Oracle Cloud Infrastructure", "OCI", "OCI Gen AI", "Oracle 23AI",
        "AWS", "EC2", "Lambda", "Cognito", "Bedrock", "Bedrock Agents", "GCP",
        # Databases
        "Oracle DB", "ADW", "ATP", "MySQL", "MongoDB", "QDrant", "Weaviate", "DynamoDB",
        # Frameworks
        "FastAPI", "Flask", "Express.js",
        # Tools
        "Git", "Docker", "Streamlit", "Chainlit", "Kubernetes",
        # Other
        "Text-to-SQL", "OCR", "ERP Systems", "API Development", "Websockets",
        "CI/CD", "Automation", "Multi-agent Systems"
    ],
    
    # Projects
    "projects": [
        {
            "name": "PRPO (Purchase Requisitions Orders) ERP AI Agent",
            "description": "Built PRPO agent using OCI Gen AI Grok & Maverick models as Text-to-SQL engines hosted on Kubernetes for ERP systems. Enabled retrieval of PO, GRN, Receipts, etc., with advanced template-level retrieval from ATP. Improved procurement query resolution efficiency by 40% across ERP deployments in ME & Europe regions.",
            "technologies": ["OCI Gen AI", "Kubernetes", "Text-to-SQL", "ATP", "ERP"]
        },
        {
            "name": "HRMS & Financial Expense AI ERP Agent",
            "description": "Developed AI-powered HRMS & Financial agents hosted on Kubernetes integrated with ERP system. Automated leave, expense, and document submissions via OCI Gen AI, improving workflow automation. Reduced manual HR/finance effort by 35% for 500+ active users.",
            "technologies": ["OCI Gen AI", "Kubernetes", "ERP", "Automation"]
        },
        {
            "name": "Disaster Recovery (DR) Setup for Cloud Workloads",
            "description": "Designed automated DR pipelines for OCI Functions, API Gateways, & Integrations. Ensured replication across India & Europe regions, strengthening continuity and compliance. Reduced Recovery Time Objective (RTO) by 45%, improving resilience.",
            "technologies": ["OCI", "DR", "API Gateway", "Cloud Functions"]
        },
        {
            "name": "MCP Server on AWS Lambda with Bedrock Integration",
            "description": "Created MCP server using AWS Lambda with Cognito authorization and API Gateway. Integrated Amazon Bedrock with DynamoDB as a unified querying layer. Enabled seamless retrieval of data from 200+ APIs, significantly improving data accessibility.",
            "technologies": ["AWS Lambda", "Bedrock", "DynamoDB", "API Gateway", "Cognito"]
        }
    ],
    
    # Achievements
    "achievements": [
        "Winner, Hackzon 2022 — Group Innovation Hackathon, NHCE",
        "Runner-Up, Builders Camp Hackathon 2023 — AWS & Intel",
        "Runner-Up, Code Your Fighter (Phaseshift 2022), BMS College",
        "Second Runner-Up, NMIT Hacks 2023 — 48-hour Intercollegiate Hackathon",
        "Participated in 15+ Hackathons & Competitions"
    ],
    
    # Certifications (optional)
    "certifications": [
        # Add any certifications here if available
    ],
    
    # Job Preferences
    "preferred_job_titles": [
        "AI Engineer",
        "Machine Learning Engineer",
        "Generative AI Engineer",
        "AI/ML Consultant",
        "Software Engineer - AI/ML",
        "Backend Developer",
        "Full Stack Developer"
    ],
    
    "preferred_locations": [
        "Remote",
        "Bangalore, India",
        "India",
        "Europe",
        "Middle East"
    ],
    
    # Salary Expectations (optional, only if required by application)
    "salary_expectation_min": "180000",  # Fill as needed
    "salary_expectation_max": "180000",  # Fill as needed
    "salary_currency": "INR",  # or "USD" for international roles
    
    # Availability
    "notice_period": "Immediate",  # Adjust based on current employment status
    "available_start_date": "",  # e.g., "2024-12-01" or leave empty
    
    # Common Screening Question Answers
    "screening_answers": {
        "authorized_to_work_india": True,
        "authorized_to_work_us": False,  # Adjust based on visa status
        "require_visa_sponsorship_india": False,  # For international roles
        "require_visa_sponsorship_us": True,
        "willing_to_relocate": True,
        "comfortable_with_remote": True,
        "years_of_python_experience": 2,  # Including academic projects
        "years_of_javascript_experience": 2,
        "years_of_ai_ml_experience": 2,
        "years_of_cloud_experience": 1.5,
        "have_bachelors_degree": True,
        "have_masters_degree": False,
        "experience_with_llms": True,
        "experience_with_langchain": True,
        "experience_with_oci": True,
        "experience_with_aws": True,
        "experience_with_kubernetes": True,
    },
    
    # References (optional)
    "references": [
        # {
        #     "name": "Reference Name",
        #     "title": "Senior Engineer",
        #     "company": "Company Name",
        #     "email": "reference@example.com",
        #     "phone": "+91-XXXXXXXXXX"
        # }
    ],
}

def validate_user_details():
    """Validate that required fields are filled in."""
    required_fields = [
        "first_name", "last_name", "email", "phone",
        "location", "resume_path", "experience_summary"
    ]
    
    missing_fields = []
    for field in required_fields:
        if not USER_DETAILS.get(field) or USER_DETAILS[field] in ["", "your.email@example.com", "+1-555-010-5555"]:
            missing_fields.append(field)
    
    if missing_fields:
        print("⚠️  WARNING: The following required fields need to be updated in user_context.py:")
        for field in missing_fields:
            print(f"   - {field}")
        print()
    
    return len(missing_fields) == 0

# Validate on import
if __name__ != "__main__":
    validate_user_details()
