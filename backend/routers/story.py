import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session


from db.database import get_db, SessionLocal
#from backend.db import crud, models
#from backend.utils import auth, utils
#from backend.schemas import story as story_schema

from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryResponse,
    CompleteStoryNodeResponse,
    CreateStoryRequest
)
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator



router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    
    # Set the session_id cookie if it was newly generated
    response.set_cookie(key="session_id", value=session_id, httponly=True)
     
    job_id = str(uuid.uuid4())

    job = StoryJob(
            job_id=job_id,
            session_id=session_id,
            theme=request.theme,
            status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job) # Refresh the job instance to get the generated ID and timestamps
           
        

   # Start the background task to generate the story
    background_tasks.add_task(
        generate_story_task, 
        job_id = job_id, 
        theme = request.theme,
        session_id = session_id
    ) 
    return job


def generate_story_task(job_id: str, theme: str, session_id: str):
    # Simulate story generation (replace with actual logic)
    db = SessionLocal()

    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first() # Fetch the job from the database
        if not job:
            return

    
        job.status = "Processing" # Update job status to "Processing"
        db.commit()


        story = StoryGenerator.generate_story(db, session_id, theme) ### Now Replaced with actual story generation logic based on the theme
        

        job.story_id = story.id ### Replaced with the actual generated story ID
        job.status = "Completed" # Update job status to "Completed"
        job.completed_at = datetime.now() # Set the completion timestamp
        db.commit()
    except Exception as e:
        job.status = "Failed" # Update job status to "Failed" in case of an error
        job.completed_at = datetime.now() # Set the completion timestamp
        job.error = str(e) # Store the error message in the job record
        db.commit() # Ensure the job status is updated in case of an error
    finally:
        db.close() # Ensure the database session is closed after the task is completed



@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    
    # Fetch the story nodes and their content
    complete_story = build_complete_story_tree(db, story)
    return complete_story

# Helper function to build the complete story tree
def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:  
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
             id=node.id,
             content=node.content,
             is_ending=node.is_ending,
             is_winning_ending=node.is_winning_ending,
             options=node.options
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found")

    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )




