FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN addgroup --system agent && adduser --system --ingroup agent agent
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && mkdir -p /data \
    && chown -R agent:agent /app /data
COPY . .
USER agent
EXPOSE 8000
# Use read-only root FS at runtime; write to /data via volume
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
