FROM python:3.14.0

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Ensure the instance folder exists inside the container
RUN mkdir -p /app/instance

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host", "0.0.0.0"]