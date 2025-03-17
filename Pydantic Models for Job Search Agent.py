from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"


class UserPreferences(BaseModel):
    """User preferences for job search."""
    job_titles: List[str] = Field(..., min_items=1, description="List of job titles to search for")
    skills: List[str] = Field(..., min_items=1, description="List of user skills")
    location: str = Field(..., min_length=2, description="Desired job location")
    remote: bool = Field(False, description="Whether remote jobs are preferred")
    min_salary: Optional[int] = Field(None, gt=0, description="Minimum expected salary")
    experience_level: ExperienceLevel = Field(ExperienceLevel.ENTRY, description="Experience level")



class JobListing(BaseModel):
    """Job listing data structure."""
    title: str = Field(..., min_length=2, description="Job title")
    company: str = Field(..., min_length=2, description="Company name")
    location: str = Field(..., min_length=2, description="Job location")
    description: str = Field(..., description="Job description")
    salary_range: Optional[str] = Field(None, description="Salary range")
    url: str = Field(..., description="Job listing URL")
    date_posted: datetime = Field(..., description="Date job was posted")
    skills_required: List[str] = Field(default_factory=list, description="List of required skills")
    match_score: Optional[float] = Field(None, ge=0, le=100, description="Match score (0-100)")


class AgentState(BaseModel):
    """State object for the job search agent workflow."""
    user_preferences: UserPreferences
    job_listings: List[JobListing] = Field(default_factory=list)
    filtered_listings: List[JobListing] = Field(default_factory=list)
    recommendations: List[JobListing] = Field(default_factory=list)
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list, description="List of error messages")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Last updated timestamp")