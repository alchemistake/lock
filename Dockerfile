# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1
ENV SQLITE_DB_PATH=/data/clicks.db

# Create a volume for persistent data
VOLUME /data

# Run app.py when the container launches
CMD ["python", "app/main.py"]