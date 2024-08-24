# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install the system dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc

# Install any dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app.api.app:get_app", "--host", "0.0.0.0", "--port", "8000"]
