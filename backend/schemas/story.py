from typing import List, Optional, Dict 
from datetime import datetime
from pydantic import BaseModel

# StoryOptionsSchema defines the structure for story options, including the option text and the next story ID it leads to.
class StoryOptionsSchema(BaseModel):
    text: str  # The text displayed for the option
    node_id: Optional[int]  # The ID of the next story node this option leads to, if applicable

# StoryNodeBase defines the base structure for a story node, including the content of the node and flags to indicate if it's an ending or winning point in the story.
class StoryNodeBase(BaseModel):
        content: str  # The content of the story node
        is_ending: bool = False  # Indicates if this node is an ending point in the story
        is_winning_ending: bool = False  # Indicates if this node is a winning point in the story


class CompleteStoryNodeResponse(StoryNodeBase):
    id: int  # The unique identifier for the story node
    options: List[StoryOptionsSchema] = []  # A list of options available at this story node


    class Config:
        from_attributes = True  # Allows the model to be created from ORM objects, enabling compatibility with database models.

class StoryBase(BaseModel):
    title: str  # The title of the story
    session_id: Optional[str] = None  # An optional session ID for tracking user sessions


    class Config:
        from_attributes = True  # Allows the model to be created from ORM objects, enabling compatibility with database models.

# CreateStoryRequest defines the structure for the request body when creating a new story, including the theme of the story.
class CreateStoryRequest(BaseModel):
    theme: str  # The theme of the story


# CompleteStoryResponse defines the structure for the response when retrieving a complete story, including the story's metadata and all associated story nodes.
class CompleteStoryResponse(StoryBase):
    id: int  # The unique identifier for the story
    created_at: datetime  # The timestamp when the story was created
    #updated_at: datetime  # The timestamp when the story was last updated
    root_node: CompleteStoryNodeResponse  # The root node of the story, which is the starting point of the story
    all_nodes: Dict[int, CompleteStoryNodeResponse] # A list of all story nodes associated with this story


    class Config:
        from_attributes = True  # Allows the model to be created from ORM objects, enabling compatibility with database models.