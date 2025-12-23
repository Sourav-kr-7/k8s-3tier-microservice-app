FROM python:3.11-slim

# Keep images lean and logs unbuffered for containers.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code last to maximize layer cache reuse.
COPY app.py .

EXPOSE 5000
# Gunicorn is production-grade; Flask dev server stays in app.py for local runs.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]

