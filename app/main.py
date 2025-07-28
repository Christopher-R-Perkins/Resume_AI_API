from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.router import api_router

app = FastAPI(
    title="Resume AI API",
    description="A FastAPI application for resume processing and AI analysis",
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

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Serve the main web interface."""
    return FileResponse("static/index.html")

@app.get("/api")
async def api_root():
    """API root endpoint that returns a welcome message."""
    return {"message": "Welcome to Resume AI API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Resume AI API"}

@app.get("/api/v1/status")
async def api_status():
    """API status endpoint."""
    return {
        "api_version": "1.0.0",
        "status": "operational",
        "endpoints": [
            "/",
            "/health",
            "/api/v1/status",
            "/api/v1/bullet",
            "/docs",
            "/redoc"
        ]
    } 