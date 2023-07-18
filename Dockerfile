# Base image
FROM python:3.9

# Set working directory
WORKDIR /src

# Copy requirements.txt to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port
EXPOSE 5000

# Start the Flask application
CMD ["python", "src.py"]
