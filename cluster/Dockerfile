# Quetzl-Core Agent Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir requests
CMD ["python", "quetzl_ml_python_cluster.py"]
