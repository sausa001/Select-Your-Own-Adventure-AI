from typing  import Optional
from datetime import datetime
from pydantic import BaseModel

# StoryJobBase defines the base structure for a story job, including the theme of the story job.
class StoryJobBase(BaseModel):
    theme: str  # The theme of the story job


# StoryJobResponse defines the structure for the response body when retrieving a story job, including all relevant details.
class StoryJobResponse(BaseModel):
    job_id: str  # The unique identifier for the story job
    status: str  # The current status of the story job (e.g., "pending", "in_progress", "completed")
    created_at: datetime  # The timestamp when the story job was created
    story_id: Optional[int] = None  # The ID of the story associated with this job, if completed
    completed_at: Optional[datetime] = None  # The timestamp when the story job was completed, if applicable
    error: Optional[str] = None  # An optional error message if the job failed


    class Config:
        from_attributes = True  # Allows the model to be created from ORM objects, enabling compatibility with database models.



# StoryJobCreate defines the structure for the request body when creating a new story job, inheriting all fields from StoryJobBase.
class StoryJobCreate(StoryJobBase):
    pass  # Inherits all fields from StoryJobBase, used for creating a new story job