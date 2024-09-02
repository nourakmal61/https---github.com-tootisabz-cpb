# Use the official Python image as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies

RUN pip install pillow==10.4.0
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files to the container
COPY . /app

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]