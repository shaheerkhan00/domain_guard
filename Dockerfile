# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install fastapi uvicorn requests

# Copy your API code
COPY main.py .

# Expose the API port
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]