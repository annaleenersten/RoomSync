FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy backend code into container
COPY code/backend/ /app/backend

# Copy frontend code into container
COPY code/frontend/ /app/frontend

# Copy requirements file from backend
COPY code/backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set working directory to backend (so python app.py works)
WORKDIR /app/backend

# Expose port Flask uses
EXPOSE 5000

CMD ["python", "app.py"]