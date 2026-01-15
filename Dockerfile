FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the entrypoint executable and expose the app port
RUN chmod +x /app/entrypoint.sh
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
