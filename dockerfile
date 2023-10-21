# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY app /app/

# Expose the port on which your Django application will run (e.g., 8000)
EXPOSE 8000

# Run your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
