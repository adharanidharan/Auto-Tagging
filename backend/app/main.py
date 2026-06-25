from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.routes import auth, questions
from services.topic_learning_service import initialize_topics

load_dotenv()

app = FastAPI(
    title="Smart Similar Question Finder API",
    description="API for the AI-powered EdTech application",
    version="1.0.0"
)

# Configure CORS for local development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    await initialize_topics()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Include routers matching target API routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(questions.router, prefix="/api/questions", tags=["questions"])
app.include_router(questions.topics_router, prefix="/api/topics", tags=["topics"])
app.include_router(questions.feedback_router, prefix="/api/feedback", tags=["feedback"])
app.include_router(questions.discovered_topics_router, prefix="/api/discovered-topics", tags=["discovered-topics"])

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Similar Question Finder API"}
