import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import logging


class LLMService:
    """Service for LLM-powered text processing and analysis."""

    def __init__(self, api_key: str = None):
        """Initialize the LLM service with dynamic model selection."""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.models = {
            "basic": "gpt-3.5-turbo",  # Faster & cheaper for simple tasks
            "advanced": "gpt-4-turbo"  # More accurate for deep analysis
        }
        
        logging.basicConfig(level=logging.INFO)
        logging.info("LLMService initialized with dynamic model selection.")
    
    def _get_llm(self, task_type: str):
        """Return the appropriate LLM model based on the task type."""
        model_name = self.models.get(task_type, "gpt-3.5-turbo")
        return ChatOpenAI(api_key=self.api_key, model=model_name, temperature=0.2)
    
    def _handle_error(self, error: Exception):
        logging.error("Error occurred: %s", error)
        raise error

    def extract_skills_from_job(self, job_description: str) -> List[str]:
        """Extract required skills from a job description."""
        if not job_description.strip():
            raise ValueError("Job description cannot be empty.")

        prompt = f"""
        Extract the key skills, technologies, and requirements from this job description:
        
        {job_description}
        
        Return only a list of skills and requirements, separated by commas.
        Focus on technical skills, tools, programming languages, and specific qualifications.
        """
        
        try:
            llm = self._get_llm("basic")  # Use GPT-3.5 for speed
            response = llm.invoke([HumanMessage(content=prompt)])
            skills_text = response.content.strip()
        except Exception as e:
            self._handle_error(e)

        # Process the skills
        skills = [skill.strip() for skill in skills_text.split(",") if skill.strip()]
        return skills

    def generate_job_insights(self, user_skills: List[str], job_titles: List[str],
                              location: str, experience_level: str,
                              top_jobs: List[Dict[str, Any]], common_skills: Dict[str, int]) -> str:
        """Generate insights and recommendations based on job search results."""
        if not top_jobs:
            raise ValueError("No job data provided for insights.")

        top_jobs_text = "\n".join([f"#{i+1}: {job['title']} at {job['company']} (Match: {job['match_score']:.2f})"
                                   for i, job in enumerate(top_jobs[:5])])

        skills_summary = ", ".join([f"{skill} ({count})" for skill, count in 
                                    sorted(common_skills.items(), key=lambda x: x[1], reverse=True)[:10]])

        prompt = f"""
        Based on the job search results, provide insights and recommendations for the user.
        
        User profile:
        - Job titles of interest: {', '.join(job_titles)}
        - Skills: {', '.join(user_skills)}
        - Location: {location}
        - Experience: {experience_level}
        
        Top matching jobs:
        {top_jobs_text}
        
        Most in-demand skills from these listings:
        {skills_summary}
        
        Provide:
        1. Overall market insights for these roles
        2. Skill gap analysis (comparing user skills with job requirements)
        3. Application strategy recommendations
        4. 2-3 suggested next steps
        
        Keep your response concise but informative.
        """
        
        try:
            llm = self._get_llm("advanced")  # Use GPT-4 for better analysis
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content.strip()
        except Exception as e:
            self._handle_error(e)

    def generate_resume_suggestions(self, job_description: str, user_skills: List[str]) -> str:
        """Generate resume tailoring suggestions for a specific job."""
        if not job_description or not user_skills:
            raise ValueError("Job description and user skills are required for generating resume suggestions.")
        
        prompt = f"""
        Help the user tailor their resume for this job:
        
        Job Description:
        {job_description}
        
        User's Current Skills:
        {', '.join(user_skills)}
        
        Provide specific suggestions to optimize their resume for this role, including:
        1. Key skills to emphasize
        2. Experience they should highlight
        3. Potential gaps they should address
        4. Keywords to include for ATS systems
        
        Be specific and actionable.
        """
        
        try:
            llm = self._get_llm("advanced")  # Use GPT-4 for resume optimization
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content.strip()
        except Exception as e:
            self._handle_error(e)