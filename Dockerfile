FROM python:3.10-slim-buster

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn explicitly
RUN pip install gunicorn

# Copy the rest of the application
COPY app.py .
COPY app ./app

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]