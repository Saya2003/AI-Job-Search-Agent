import logging
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph

# Configure logging
logging.basicConfig(level=logging.INFO)

class JobSearchWorkflow:
    def __init__(self, scraper, llm_service):
        self.scraper = scraper
        self.llm_service = llm_service
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("scrape_jobs", self._scrape_jobs)
        workflow.add_node("process_jobs", self._process_jobs)
        workflow.add_node("filter_and_rank", self._filter_and_rank)
        workflow.add_edge("scrape_jobs", "process_jobs")
        workflow.add_edge("process_jobs", "filter_and_rank")
        workflow.set_entry_point("scrape_jobs")
        return workflow.compile()

    def _scrape_jobs(self, state: AgentState) -> AgentState:
        try:
            linkedin_jobs = self.scraper.scrape_linkedin_jobs(state.user_preferences)
            state.job_listings.extend(linkedin_jobs)
            
            if len(linkedin_jobs) < 30:
                indeed_jobs = self.scraper.scrape_indeed_jobs(state.user_preferences)
                state.job_listings.extend(indeed_jobs)
            
            state.messages.append({"role": "system", "content": f"Scraped {len(state.job_listings)} job listings."})
        except Exception as e:
            logging.error(f"Job scraping failed: {str(e)}", exc_info=True)
            state.error = f"Error scraping job listings: {str(e)}"
        return state

    def _process_jobs(self, state: AgentState) -> AgentState:
        if not state.job_listings:
            return state
        
        job_descriptions = [job.description for job in state.job_listings[:30] if len(job.description) >= 100]
        
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.llm_service.extract_skills_from_job, job_descriptions))
        
        for i, skills in enumerate(results):
            state.job_listings[i].skills_required = skills
        return state

    def _filter_and_rank(self, state: AgentState) -> AgentState:
        logging.info("Starting job filtering and ranking...")
        
        user_skills = np.array([skill.lower() for skill in state.user_preferences.skills])
        job_scores = []
        
        for job in state.job_listings:
            job_skills = np.array([skill.lower() for skill in job.skills_required])
            skills_match = np.intersect1d(user_skills, job_skills).size / job_skills.size if job_skills.size else 0
            title_match = any(title.lower() in job.title.lower() for title in state.user_preferences.job_titles)
            title_score = 1.0 if title_match else 0.5
            location_match = 1.0 if state.user_preferences.location.lower() in job.location.lower() else 0.5
            job.match_score = (skills_match * 0.6) + (title_score * 0.2) + (location_match * 0.2)
            
            if job.match_score >= 0.4:
                job_scores.append(job)
        
        state.filtered_listings = sorted(job_scores, key=lambda x: x.match_score, reverse=True)[:10]
        logging.info(f"Top {len(state.filtered_listings)} jobs selected.")
        return state

    def run(self, user_preferences: UserPreferences) -> Dict[str, Any]:
        initial_state = AgentState(user_preferences=user_preferences)
        
        try:
            final_state = self.workflow.invoke(initial_state)
        except Exception as e:
            logging.error(f"Workflow execution failed: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "recommendations": [],
                "insights": "An error occurred during job search. Please try again.",
                "total_jobs_found": 0,
                "relevant_matches": 0
            }
        
        if not final_state.filtered_listings:
            return {
                "recommendations": [],
                "insights": "No relevant jobs found. Try adjusting search criteria.",
                "total_jobs_found": len(final_state.job_listings),
                "relevant_matches": 0
            }
        
        return {
            "recommendations": [job.model_dump() for job in final_state.filtered_listings],
            "insights": final_state.messages[-1]["content"] if final_state.messages else "No insights generated.",
            "total_jobs_found": len(final_state.job_listings),
            "relevant_matches": len(final_state.filtered_listings)
        }