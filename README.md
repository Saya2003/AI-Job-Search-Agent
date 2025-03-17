AI Job Search Agent

An AI-powered job search assistant that helps users find relevant job opportunities by analyzing their resumes, skills, and preferences. Built using **LangGraph**, **Apify**, and **LLMs**, this agent intelligently scrapes job listings, ranks them based on relevance, and provides structured insights.

🚀 Features

- Resume Parsing & Skill Extraction: Extracts skills, experience, and key insights from resumes.
- Multi-Platform Job Search: Scrapes job listings from supported platforms.
- Intelligent Job Matching: Uses LLM-based analysis to rank job listings based on relevance.
- Personalized Recommendations: Suggests job opportunities tailored to user preferences.
- Automated Filtering & Scoring: Removes duplicate postings and highlights top matches.
- Structured JSON Output: Provides clean, structured job search results.

💡 Use Cases

- Job Seekers: Get personalized job listings that match your skills and career goals.
- Recruiters: Identify top candidates and suggest relevant job positions.
- Career Coaches: Offer AI-driven insights for job search and skill improvement.
- Market Researchers: Analyze hiring trends and skill demand across industries.

🔧 Input Parameters

 Field       Type      Description                                              
 resume      String   User’s resume text to analyze                            
 location    String   Preferred job location (default: "Remote")              
 jobType     String   Type of job (e.g., "full-time", "part-time", "contract") 
 keywords    String   Additional job search keywords                           
 modelName   String   LLM model to use for analysis (default: "gpt-4-turbo")         

📊 Output

The AI Agent provides structured JSON output with:

1. Search Summary

   - Number of relevant job matches
   - Insights into top industries hiring for given skills

2. Top Matching Jobs

   - Job title, company, and location
   - Salary information (if available)
   - Relevance score (0-1 scale)
   - Application link

3. AI-Powered Recommendations

   - Suggested job application strategies
   - Career improvement tips based on job market analysis

📚 Example Usage

Input:

json
{
    "resume": "Experienced software engineer with Python, AI, and data analysis skills...",
    "location": "New York",
    "jobType": "full-time",
    "keywords": "AI, Machine Learning, Python",
    "modelName": "gpt-4"
}
```

Output:

json
{
    "summary": "Found 12 AI-related job listings in New York...",
    "jobs": [
        {
            "title": "Machine Learning Engineer",
            "company": "Tech Innovations Inc.",
            "location": "New York, NY",
            "salary": "$120,000 - $150,000",
            "match_score": 0.94,
            "url": "https://..."
        }
    ],
    "recommendations": [
        "Consider applying for jobs with AI model deployment experience.",
        "Expand search to remote roles for better opportunities."
    ]
}


🛠️ Customization

- Modify job search sources by adding new APIs in src/Services/Apify_Job_Scraper_Service.py.
- Adjust the matching algorithm for personalized ranking in src/Workflows/LangGraph_Job_Search_Workflow.py.
- Change the output structure in main.py to fit your data needs.

📈 Performance Optimization

- Parallelized job searches for speed
- Smart filtering to avoid duplicates
- Caching for faster query processing
- API rate limiting for stability

🔗 Related Apify Actors

- [LinkedIn Jobs Scraper](https://apify.com/krandiash/linkedin-jobs-scraper)
- [Indeed Job Scraper](https://apify.com/krandiash/indeed-scraper)
- [Dice Job Scraper](https://apify.com/mohamedgb00714/dicecom-job-scraper)

💬 Support & Documentation

- Apify Docs: [https://docs.apify.com/](https://docs.apify.com/)
- LangGraph Docs: [https://github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- Join the Community: [Apify Discord](https://discord.com/invite/jyEM2PRvMU)

📝 License

Apache 2.0 License