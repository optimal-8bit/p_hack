import logging
import subprocess
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
load_dotenv()

from api.routes import router
from voice.voice_routes import voice_router
from api.doctor_routes import router as doctor_router
from database.db import create_tables
from models.emotion_classifier import get_emotion_model
from models.intent_classifier import get_intent_model
from models.translator import get_translation_manager
from pipeline.orchestrator import get_orchestrator
from voice.transcriber import get_transcriber
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Mental Health Chatbot API",
    description="Offline, privacy-first, multilingual AI mental health chatbot",
    version="1.0.0"
)

# Add CORS middleware (allow all for hackathon demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)
app.include_router(voice_router)
app.include_router(doctor_router)

# Include auth routes
from api.auth_routes import router as auth_router
app.include_router(auth_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize all components on startup"""
    logger.info("=" * 60)
    logger.info("Starting Mental Health Chatbot Backend")
    logger.info("=" * 60)
    
    # 1. Create database tables
    logger.info("Creating database tables...")
    await create_tables()
    
    # 2. Load emotion classifier
    logger.info("Loading emotion classifier...")
    emotion_model = get_emotion_model()
    if emotion_model.is_loaded():
        logger.info("✓ Emotion classifier loaded (ONNX)")
    else:
        logger.warning("⚠ Emotion classifier using rule-based fallback")
    
    # 3. Load intent classifier
    logger.info("Loading intent classifier...")
    intent_model = get_intent_model()
    if intent_model.is_loaded():
        logger.info("✓ Intent classifier loaded (ONNX)")
    else:
        logger.warning("⚠ Intent classifier using rule-based fallback")
    
    # 4. Initialize translation manager (lazy-loaded)
    logger.info("Initializing translation manager...")
    translation_manager = get_translation_manager()
    logger.info("✓ Translation manager initialized (models will be lazy-loaded)")
    
    # 5. Initialize orchestrator
    logger.info("Initializing chat orchestrator...")
    orchestrator = get_orchestrator()
    logger.info("✓ Chat orchestrator initialized")
    
    # 6. Check ffmpeg availability
    logger.info("Checking ffmpeg availability...")
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            logger.info("✓ ffmpeg is available")
        else:
            logger.warning(
                "⚠ ffmpeg not found — only .wav audio will work reliably. "
                "Install ffmpeg from https://ffmpeg.org/download.html"
            )
    except Exception as e:
        logger.warning(
            f"⚠ ffmpeg check failed: {e}. "
            "Only .wav audio will work reliably. "
            "Install ffmpeg from https://ffmpeg.org/download.html"
        )
    
    # 7. Pre-load Whisper model
    logger.info("Pre-loading Whisper model...")
    try:
        transcriber = get_transcriber()
        if transcriber.is_loaded():
            logger.info("✓ Whisper model loaded")
        else:
            logger.warning("⚠ Whisper model failed to load — voice features will not work")
    except Exception as e:
        logger.warning(f"⚠ Whisper model loading failed: {e}")
    
    logger.info("=" * 60)
    logger.info("Backend startup complete!")
    logger.info(f"Server running at http://{config.HOST}:{config.PORT}")
    logger.info("API docs available at http://localhost:8000/docs")
    logger.info("=" * 60)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with simple HTML page"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mental Health Chatbot API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
            }
            .status {
                background: #e8f5e9;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            a {
                color: #3498db;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .endpoint {
                background: #f8f9fa;
                padding: 10px;
                margin: 10px 0;
                border-left: 3px solid #3498db;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Mental Health Chatbot API</h1>
            <div class="status">
                <strong>Status:</strong> ✓ Server is running
            </div>
            
            <h2>API Documentation</h2>
            <p>Interactive API documentation is available at:</p>
            <ul>
                <li><a href="/docs">Swagger UI</a></li>
                <li><a href="/redoc">ReDoc</a></li>
            </ul>
            
            <h2>Key Endpoints</h2>
            <div class="endpoint">
                <strong>POST /api/chat</strong> - Send a message to the chatbot
            </div>
            <div class="endpoint">
                <strong>POST /api/voice/chat</strong> - Send voice message with audio-fused emotion detection
            </div>
            <div class="endpoint">
                <strong>GET /api/voice/health</strong> - Check voice pipeline status
            </div>
            <div class="endpoint">
                <strong>GET /api/health</strong> - Check system health and model status
            </div>
            <div class="endpoint">
                <strong>GET /api/session/{session_id}/history</strong> - Get conversation history
            </div>
            <div class="endpoint">
                <strong>GET /api/supported-languages</strong> - List supported languages
            </div>
            
            <h2>Features</h2>
            <ul>
                <li>✓ Offline AI inference (no cloud calls)</li>
                <li>✓ Crisis detection and safety responses</li>
                <li>✓ Multilingual support (English, Hindi, French, Spanish)</li>
                <li>✓ Emotion and intent classification</li>
                <li>✓ Context-aware responses</li>
                <li>✓ Voice input with audio-fused emotion detection</li>
                <li>✓ Emotional incongruence detection</li>
            </ul>
            
            <h2>Test UI</h2>
            <p>Open <code>frontend_test/index.html</code> in your browser for a simple test interface.</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level="info"
    )
