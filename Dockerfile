# Stage 1: Build frontend
FROM node:20 AS frontend-builder
WORKDIR /frontend
COPY frontend/blogpostui/package*.json ./
RUN npm install
COPY frontend/blogpostui ./
RUN npm run build

# Stage 2: Setup Django backend
FROM python:3.11
WORKDIR /backend/blogpost

# Install backend dependencies
COPY backend/requirements.txt /backend/
RUN pip install --no-cache-dir -r /backend/requirements.txt

# Copy all backend code
COPY backend/ /backend/

# Copy frontend build to Django static files
COPY --from=frontend-builder /frontend/build /backend/static

# Expose port
EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python manage.py migrate && gunicorn blogpost.wsgi:application --bind 0.0.0.0:8000"]
