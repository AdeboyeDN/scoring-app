FROM python:3.10-slim

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose Ray Serve default HTTP port
EXPOSE 8000

# Run the app
CMD ["python", "app.py"]
