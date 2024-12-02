# Build stage
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy built application from builder stage
COPY --from=builder /app .
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# Expose the port
EXPOSE 3000

# Start the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]
