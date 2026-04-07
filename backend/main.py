from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers import story, job

from db.database import create_tables # Create database tables on startup

create_tables()


# Create FastAPI app
app = FastAPI(
    title="Select Your Own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url= "/redoc"
)

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Allow all origins for development (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)



# Define a simple route for testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",  host="0.0.0.0", port=8000, reload=True)

