# Use the official Python image as a base
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /apihub

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./apihub /apihub

# Set PYTHONPATH to make sure /apihub is in the Python module path
ENV PYTHONPATH=/apihub

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "manage:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]