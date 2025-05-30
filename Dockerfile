# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the app.py into container
COPY app.py .

# Install Flask
RUN pip install --no-cache-dir flask

# Expose port 8080
EXPOSE 8080

# Command to run the app
CMD ["python", "app.py"]
