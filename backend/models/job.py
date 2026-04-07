from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db.database import Base

class StoryJob(Base):
    __tablename__ = "story_jobs"

    id = Column(Integer, primary_key=True, index=True)# Unique identifier for the job
    job_id = Column(String, unique=True, index=True) # Unique job ID for tracking
    story_id = Column(Integer, nullable=True)  # Link to the story being generated
    session_id = Column(String, index=True)  # To track user sessions for job management
    theme = Column(String)  # Theme for the story generation
    status = Column(String)  # Job status (e.g., pending, in_progress, completed, failed)
    error = Column(String, nullable=True)  # Error message if the job fails
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)  # Timestamp for when the job is completed