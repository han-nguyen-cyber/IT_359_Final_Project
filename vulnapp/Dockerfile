FROM python:3.11-slim

# Define the working directory inside the container
# All subsequent commands (COPY, RUN, CMD) will execute from this path
WORKDIR /app

# Copy all files from the local project directory into the container's /app directory
COPY . .

# Install the Flask web framework
RUN pip install flask

# Set the default command to execute when the container starts
# This launches the Python application
CMD ["python", "app.py"]