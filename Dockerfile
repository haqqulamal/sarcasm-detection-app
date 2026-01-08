# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app_api.py .
COPY app_web.py .
COPY README.md .

# Copy model checkpoint
COPY best_checkpoint/ ./best_checkpoint/

# Expose ports
# 7860 for FastAPI backend
# 8501 for Streamlit frontend
EXPOSE 7860 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:7860/health || exit 1

# Run both services
# Start FastAPI backend in background and Streamlit frontend in foreground
CMD bash -c "python app_api.py > /tmp/api.log 2>&1 & streamlit run app_web.py --server.port=8501 --server.address=0.0.0.0"
