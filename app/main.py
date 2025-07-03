from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="SignalTap API",
    description="FastAPI backend for connecting to Rockwell Allen-Bradley CompactLogix PLCs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routes
from app.routes import plc

app.include_router(plc.router, prefix="/api", tags=["PLC"])

@app.get("/")
async def root():
    """Root endpoint for SignalTap API"""
    return {
        "message": "Welcome to SignalTap API",
        "version": "1.0.0",
        "description": "PLC Tag Management System"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SignalTap API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 