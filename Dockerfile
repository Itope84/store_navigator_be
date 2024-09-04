FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y libcairo2-dev

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn explicitly
RUN pip install gunicorn

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]