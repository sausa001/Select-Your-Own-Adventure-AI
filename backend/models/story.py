from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    session_id = Column(String, index=True, nullable=False)  # To track user sessions for story generation
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Timestamp for story creation

   # Relationship to nodes in the story
    nodes = relationship("StoryNode", back_populates="story")

# Define the StoryNode model to represent individual nodes in the story
class StoryNode(Base):
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False) # Foreign key to link to the parent story
    content = Column(String, nullable=False) # Content of the story node
    is_root = Column(Boolean, default=False) # Flag to indicate if this node is the root node of the story
    is_ending = Column(Boolean, default=False) # Flag to indicate if this node is an ending node in the story
    is_winning_ending = Column(Boolean, default=False) # Flag to indicate if this node is a winning ending in the story
    options = Column(JSON, default=list) # JSON field to store options for branching the story

    # Relationship back to the parent story
    story = relationship("Story", back_populates="nodes")

