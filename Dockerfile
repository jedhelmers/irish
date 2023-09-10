# --- Build Stage ---
FROM node:14 AS frontend-build

WORKDIR /app/frontend

# Copy package.json and package-lock.json for frontend
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the rest of the frontend files and build
COPY frontend/ ./
RUN npm run build

# --- Production Stage ---
FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install additional tools like netcat and PostgreSQL client
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy the built frontend assets from the build stage
COPY --from=frontend-build /app/frontend/build /app/frontend/build

# Copy the Django application and other necessary files
COPY . .

# Set the entry point
COPY entrypoint.sh /app/entrypoint.sh
COPY ./scripts/wait-for-it.sh /scripts/wait-for-it.sh
RUN chmod +x /app/entrypoint.sh /scripts/wait-for-it.sh
ENTRYPOINT ["/app/entrypoint.sh"]
