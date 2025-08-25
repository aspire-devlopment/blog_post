# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /backend

# Copy requirements.txt from the root and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the blogpost directory contents into the working directory
COPY blogpost/ .

# Expose port
EXPOSE 8000

# Run migrations & start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
