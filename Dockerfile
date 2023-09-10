FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install necessary utilities
RUN apt-get update \
    && apt-get install -y postgresql-client curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Copy & Setup frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build && rm -rf node_modules

# Set work directory for Django app
WORKDIR /app

# Copy the rest of the app
COPY . .

# Copy entrypoint & other necessary scripts
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY ./scripts/wait-for-it.sh /scripts/wait-for-it.sh
RUN chmod +x /scripts/wait-for-it.sh

ENTRYPOINT ["/app/entrypoint.sh"]
