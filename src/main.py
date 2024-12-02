from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import sys
import json
from pythonjsonlogger import jsonlogger
import platform

# Configure JSON logging
logger = logging.getLogger()
logHandler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter(
    '%(timestamp)s %(level)s %(name)s %(message)s %(request_id)s',
    rename_fields={'levelname': 'level', 'asctime': 'timestamp'}
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(
    title="Coolify Docker Test Python API",
    description="A test API project using FastAPI to verify Docker deployment on Coolify platform",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    # Generate request ID
    request_id = request.headers.get('X-Request-ID', str(datetime.now().timestamp()))
    
    # Log request
    logger.info(
        "Incoming request",
        extra={
            'request_id': request_id,
            'method': request.method,
            'url': str(request.url),
            'headers': dict(request.headers),
            'client': request.client.host if request.client else None
        }
    )
    
    # Process request
    start_time = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()
    
    # Log response
    logger.info(
        "Request completed",
        extra={
            'request_id': request_id,
            'duration': duration,
            'status_code': response.status_code
        }
    )
    
    response.headers['X-Request-ID'] = request_id
    return response

@app.get("/")
async def root():
    """Root endpoint returning welcome message and timestamp"""
    return {
        "status": "success",
        "message": "Welcome to the Test API",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/version")
async def version():
    """Version endpoint showing application details"""
    return {
        "version": "0.1.0",
        "framework": "FastAPI",
        "python_version": platform.python_version(),
        "platform": platform.platform()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )
