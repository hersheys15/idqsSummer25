FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Set backend as working dir for app
WORKDIR /app/backend

# Install dependencies
RUN pip install --no-cache-dir -r ../requirements.txt

# Expose port used by Flask/Gunicorn
EXPOSE 8080

# Run with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]