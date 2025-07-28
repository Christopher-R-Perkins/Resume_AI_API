# Resume AI API

A FastAPI-based application for creating powerful resume bullet points through AI assistance.

## The Story Behind This Tool

I was frustrated with existing AI tools for creating resume bullets. ChatGPT, while initially helpful, would get worse and worse as our conversation progressed - it would use context from previous discussions and couldn't stay on track. Each new bullet point would be influenced by all the previous ones, making them less focused and effective.

I created this tool to solve that problem. It generates engaging, powerful resume bullets without any external context interference. Each bullet is created fresh, ensuring maximum impact and relevance for your specific accomplishment.

## Current Focus

This project currently focuses on **one thing and does it well**: creating powerful resume bullet points. The AI generates multiple bullet variations for each accomplishment, grades them for quality, and provides visual feedback on their effectiveness.

## Features

- **AI-Powered Bullet Generation**: Creates multiple bullet point variations for each accomplishment
- **Quality Scoring**: Each bullet is automatically graded for effectiveness (0-1 scale)
- **Visual Feedback**: Color-coded score bars (Green: ≥0.9, Yellow: 0.75-0.9, Red: <0.75)
- **Web Interface**: Modern, responsive UI with form-based input and history tracking
- **Local Storage**: All generated bullets are saved locally in your browser
- **FastAPI Backend**: Robust API with automatic documentation
- **Development Script**: One-command setup and run with automatic dependency management

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- bash (for development script)
- OpenAI API key with access to reasoning models

### Environment Setup

1. **Create a `.env` file** in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=False
```

2. **Complete OpenAI identity verification** to unlock reasoning models for your organization. The AI agents use advanced reasoning capabilities that require verified accounts.

3. **Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key (required)
   - `DEBUG`: Set to `True` to enable detailed logging of AI thinking summaries and debug messages (optional, defaults to False)

### One-Command Setup and Run

The easiest way to get started is using the provided development script:

```bash
./run_dev.sh
```

This script will:
- Check for Python and pip installation
- Create a virtual environment if needed
- Install all dependencies
- Start the development server with auto-reload

## Manual Setup

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Resume_AI_API
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Server (Recommended)

**Option 1: Using the development script (easiest)**
```bash
./run_dev.sh
```

**Option 2: Manual uvicorn command**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Direct Python execution**
```bash
python main.py
```

### Production Server

For production deployment:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Custom Configuration

You can customize the server settings using environment variables:

```bash
HOST=127.0.0.1 PORT=8080 ./run_dev.sh
```

Or set them permanently:
```bash
export HOST=127.0.0.1
export PORT=8080
./run_dev.sh
```

## Web Interface

The application includes a modern web interface for interacting with the bullet generation API:

- **URL**: http://localhost:8000 (when server is running)
- **Features**:
  - **New Bullet Tab**: Create new bullet points with a form interface
  - **History Tab**: View and manage previously generated bullets
  - **Local Storage**: All generated bullets are saved locally in your browser
  - **Score Visualization**: Each bullet shows a color-coded score bar
  - **Responsive Design**: Works on desktop and mobile devices

### Web Interface Features

1. **New Bullet Creation**:
   - Form with fields for accomplished, measured, task, and optional keyword
   - Real-time API interaction with loading states
   - Automatic storage of inputs and outputs

2. **Bullet History**:
   - Browse all previously generated bullets
   - Click any history item to view full details
   - Clear history functionality
   - Persistent storage using browser localStorage

3. **Score Visualization**:
   - Color-coded score bars (Green: ≥0.9, Yellow: 0.75-0.9, Red: <0.75)
   - Numerical score display
   - Visual feedback for bullet quality

### Static File Organization

The web interface is organized in the `static/` directory for better maintainability:

- **`static/index.html`**: Main HTML structure
- **`static/styles.css`**: All CSS styling and responsive design
- **`static/app.js`**: JavaScript functionality and API interactions

This separation allows for:
- Easier maintenance and updates
- Better caching by browsers
- Cleaner code organization
- Future expansion with additional HTML pages

## API Endpoints

- `GET /` - Web interface (serves index.html)
- `GET /api` - API root endpoint with welcome message
- `GET /health` - Health check endpoint
- `GET /api/v1/status` - API status and version information
- `POST /api/v1/bullet` - Create resume bullet points from provided information
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Bullet Endpoint Usage

The `/api/v1/bullet` endpoint creates resume bullet points from provided information:

**Request:**
```json
{
  "accomplished": "increased user engagement",
  "measured": "by 25%", 
  "task": "implementing new features"
}
```

**Response:**
```json
{
  "bullet_list": [
    {
      "bullet": "Accomplished increased user engagement by implementing new features, measured by 25%",
      "rating": 0.85
    },
    {
      "bullet": "Successfully completed implementing new features resulting in increased user engagement",
      "rating": 0.78
    },
    {
      "bullet": "Delivered increased user engagement through implementing new features with measurable impact: 25%",
      "rating": 0.92
    }
  ]
}
```

## Project Structure

```
Resume_AI_API/
├── app/                    # Main application package
│   ├── main.py            # FastAPI application instance
│   ├── models/
│   │   └── bullet.py      # Bullet-related data models
│   ├── agents/
│   │   └── bullet/        # AI agents for bullet processing
│   │       ├── bullet_writing_agent.py    # Generates bullet points
│   │       └── bullet_grading_agent.py    # Grades bullet quality
│   ├── utils/             # Utility functions
│   │   ├── bullet.py      # Bullet processing utilities
│   │   └── openai.py      # OpenAI integration utilities
│   └── api/               # API package
│       ├── __init__.py    # API package initialization
│       └── v1/            # API version 1
│           ├── router.py  # V1 API router
│           └── endpoints/
│               └── bullet.py    # Bullet endpoint implementation
├── static/                # Static web assets
│   ├── index.html         # Main web interface
│   ├── styles.css         # CSS styling and responsive design
│   └── app.js             # JavaScript functionality and API interactions
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── run_dev.sh            # Development server script
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## Development

### Development Script Features

The `run_dev.sh` script provides:

- **Automatic Setup**: Creates virtual environment and installs dependencies
- **Error Handling**: Validates prerequisites and provides helpful error messages
- **Colored Output**: Clear status messages with color coding
- **Auto-reload**: Watches for file changes and restarts server automatically
- **Configurable**: Supports environment variables for customization

### Adding New Endpoints

To add new endpoints, create a new file in `app/api/v1/endpoints/` and add it to the router:

1. Create a new endpoint file (e.g., `app/api/v1/endpoints/resume.py`):
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/resume")
async def get_resume():
    return {"message": "Resume endpoint"}
```

2. Add the endpoint to the router in `app/api/v1/router.py`:
```python
from app.api.v1.endpoints import resume

api_router.include_router(resume.router, tags=["resume"])
```

### Environment Variables

For production deployment, consider using environment variables for configuration:

```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export DEBUG=false
```

### Dependencies

Current dependencies (see `requirements.txt`):
- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `pydantic==2.5.0` - Data validation

## Future Improvements

While this tool currently fits my needs perfectly, here are some potential enhancements that could be added:

### Possible Features
- **Full Resume Creation**: Complete resume generation with multiple sections
- **LaTeX Template Generation**: Export to professional LaTeX resume templates
- **Job Posting Matching**: Analyze job descriptions and tailor bullets accordingly
- **Database Integration**: Store and manage multiple resumes and bullet libraries
- **Industry-Specific Templates**: Tailored bullet styles for different sectors
- **A/B Testing**: Compare different bullet variations for effectiveness
- **Export Options**: PDF, Word, and other format exports

### Development Philosophy

This project follows a "do one thing well" philosophy. The current tool solves a specific problem effectively without unnecessary complexity. Updates may be few and far between as the core functionality already meets the intended use case.

## Troubleshooting

### Common Issues

1. **Permission denied on run_dev.sh**
   ```bash
   chmod +x run_dev.sh
   ```

2. **Python not found**
   - Ensure Python 3.8+ is installed and in your PATH
   - On macOS, you might need to use `python3` instead of `python`

3. **Port already in use**
   - Change the port using: `PORT=8080 ./run_dev.sh`
   - Or kill the process using the port

4. **Virtual environment issues**
   - Delete the `venv` folder and run `./run_dev.sh` again
   - The script will recreate the environment

5. **OpenAI API errors**
   - Verify your API key is correct and has sufficient credits
   - Ensure your account has completed identity verification to unlock reasoning models
   - Check the `.env` file is in the project root directory

## License

This project is licensed under the MIT License. 