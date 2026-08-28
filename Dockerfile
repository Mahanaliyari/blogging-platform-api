# Use Python 3.12 slim as the base image
FROM python:3.12-slim

# Set /app as the working directory inside the container
WORKDIR /app

# Copy requirements.txt from the project into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Start the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]