import logging
import os
from typing import List, Optional, Dict, Any
from apify_client import ApifyClient, ApifyClientAsync
from ..models import JobListing, UserPreferences
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=3600)  # Store results for 1 hour


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApifyScraper:
    """Service for scraping job listings using Apify actors."""
    
    def __init__(self, api_token: Optional[str] = None):
        """Initialize the Apify client."""
        self.api_token = api_token or os.environ.get("APIFY_API_TOKEN")
        if not self.api_token:
            raise ValueError("Apify API token is required")
        self.client = ApifyClient(self.api_token)
    
    def scrape_linkedin_jobs(self, preferences: UserPreferences, max_items: int = 50) -> List[JobListing]:
        """Scrape job listings from LinkedIn using Apify actor."""
        try:
            run_input = {
                "queries": preferences.job_titles,
                "locationOrMilesRadius": preferences.location,
                "applyLink": True,
                "maxItems": max_items
            }

            logger.info(f"Starting LinkedIn Jobs scraper for: {preferences.job_titles}")
            run = self.client.actor("hundredvisions/linkedin-jobs-scraper").call(run_input=run_input)
            
            job_listings = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                job = JobListing(
                    title=item.get("title", "Unknown"),
                    company=item.get("company", "Unknown"),
                    location=item.get("location", "Remote" if preferences.remote else "Unknown"),
                    description=item.get("description", ""),
                    salary_range=item.get("salary", None),
                    url=item.get("applyLink", item.get("link", "")),
                    date_posted=item.get("postedDate", ""),
                    skills_required=[]
                )
                job_listings.append(job)
            
            logger.info(f"Scraped {len(job_listings)} jobs from LinkedIn")
            return job_listings
            
        except Exception as e:
            logger.error(f"Error scraping LinkedIn jobs: {e}")
            return []  # Return empty list instead of raising an error
    
    def scrape_indeed_jobs(self, preferences: UserPreferences, max_items: int = 30) -> List[JobListing]:
        """Scrape job listings from Indeed using Apify actor."""
        try:
            run_input = {
                "queries": [f"{title} in {preferences.location}" for title in preferences.job_titles],
                "includeUnfilteredResults": False,
                "maxPagesPerQuery": 3,
                "proxy": {"useApifyProxy": True}
            }
            
            logger.info(f"Starting Indeed Jobs scraper for: {preferences.job_titles}")
            run = self.client.actor("dtrungtin/indeed-scraper").call(run_input=run_input)
            
            job_listings = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                job = JobListing(
                    title=item.get("title", "Unknown"),
                    company=item.get("company", {}).get("name", "Unknown"),
                    location=item.get("location", "Unknown"),
                    description=item.get("description", ""),
                    salary_range=item.get("salary", ""),
                    url=item.get("url", ""),
                    date_posted=item.get("date", ""),
                    skills_required=[]
                )
                job_listings.append(job)
            
            logger.info(f"Scraped {len(job_listings)} jobs from Indeed")
            return job_listings
            
        except Exception as e:
            logger.error(f"Error scraping Indeed jobs: {e}")
            return []

    def scrape_company_info(self, company_name: str) -> Dict[str, Any]:
        """Scrape company information using Google Search Results Scraper."""
        try:
            run_input = {
                "queries": [f"{company_name} company information", f"{company_name} reviews"],
                "maxPagesPerQuery": 1,
                "resultsPerPage": 5,
                "mobileResults": False,
                "langCode": "en",
                "countryCode": "us",
                "includeHtml": False
            }
            
            run = self.client.actor("apify/google-search-scraper").call(run_input=run_input)
            
            results = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                if "organicResults" in item:
                    results.extend(item["organicResults"][:3])
            
            logger.info(f"Scraped company info for {company_name}")
            return {"company_name": company_name, "search_results": results}
            
        except Exception as e:
            logger.error(f"Error scraping company info for {company_name}: {e}")
            return {"company_name": company_name, "search_results": []}