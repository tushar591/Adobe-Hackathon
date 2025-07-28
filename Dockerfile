# Dockerfile for Challenge 1b: Multi-Collection PDF Analysis
# Optimized for CPU-only execution on AMD64 architecture

FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the necessary NLTK and spaCy models for offline use
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
RUN python -m spacy download en_core_web_sm

# Copy your Python application code into the container
COPY *.py ./

# Copy the entire Challenge_1b directory with all its collections
COPY Challenge_1b/ ./Challenge_1b/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Define the default command to run when the container starts
CMD ["python", "main.py"]