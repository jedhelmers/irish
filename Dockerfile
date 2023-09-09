FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Install netcat
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy entry point script then run id
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY ./scripts/wait-for-it.sh /scripts/wait-for-it.sh
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /scripts/wait-for-it.sh /app/entrypoint.sh


# Set the entry point of the container
ENTRYPOINT ["/app/entrypoint.sh"]

COPY . .
