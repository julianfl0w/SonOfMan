# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

RUN apt update

RUN apt install libgtk2.0-dev pkg-config -y

# Install required packages
RUN pip install opencv-python-headless Flask requests

# Copy the current directory content into the container at /app
COPY . /app

# Define the command to run the Python script
CMD ["python", "./host.py"]
