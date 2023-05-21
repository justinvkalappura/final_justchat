# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

ENV DJANGO_SETTINGS_MODULE=justchat.settings

# Expose the port that Django runs on
# ENV PYTHONPATH=/justchat

EXPOSE 8000

# Set the entry point command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]