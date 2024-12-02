from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import sys
import json
from pythonjsonlogger import jsonlogger
import platform
import uvicorn

# Configure JSON logging
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.now().isoformat()
        log_record['level'] = record.levelname
        log_record['name'] = record.name

# Configure root logger
logger = logging.getLogger()
logHandler = logging.StreamHandler(sys.stdout)
formatter = CustomJsonFormatter(
    '%(timestamp)s %(level)s %(name)s %(message)s',
    json_indent=2  # Pretty print JSON for better readability
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Configure uvicorn access logger
uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.handlers = [logHandler]

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

def format_headers(headers):
    """Format headers for pretty printing"""
    return {k: v for k, v in headers.items()}

# Logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = request.headers.get('X-Request-ID', str(datetime.now().timestamp()))
    
    # Print request separator
    print("\n=== INCOMING REQUEST ===")
    
    # Log request details
    logger.info("Request details", extra={
        'request_id': request_id,
        'method': request.method,
        'path': request.url.path,
        'query_params': str(request.query_params),
        'headers': format_headers(request.headers),
        'client_host': request.client.host if request.client else None,
        'client_port': request.client.port if request.client else None
    })

    # Try to log request body for non-GET requests
    if request.method not in ['GET', 'HEAD']:
        try:
            body = await request.body()
            if body:
                logger.info("Request body", extra={
                    'request_id': request_id,
                    'body': body.decode()
                })
        except Exception as e:
            logger.warning(f"Could not read request body: {str(e)}")

    # Process request and measure duration
    start_time = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()

    # Log response details
    logger.info("Response details", extra={
        'request_id': request_id,
        'duration_seconds': duration,
        'status_code': response.status_code,
        'response_headers': format_headers(response.headers)
    })

    # Print request end separator
    print("=== END REQUEST ===\n")

    response.headers['X-Request-ID'] = request_id
    return response

@app.get("/")
async def root():
    """Root endpoint returning welcome message and timestamp"""
    logger.info("Accessing root endpoint")
    return {
        "status": "success",
        "message": "Welcome to the Test API",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/version")
async def version():
    """Version endpoint showing application details"""
    logger.info("Accessing version endpoint")
    return {
        "version": "0.1.0",
        "framework": "FastAPI",
        "python_version": platform.python_version(),
        "platform": platform.platform()
    }

if __name__ == "__main__":
    print("\n=== Starting FastAPI Server ===")
    logger.info("Server configuration", extra={
        'host': '0.0.0.0',
        'port': 3000,
        'environment': 'development' if "--reload" in sys.argv else 'production'
    })
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )
