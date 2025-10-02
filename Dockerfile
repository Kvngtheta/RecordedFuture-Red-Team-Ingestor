FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy cryptography requests typer
EXPOSE 8000
CMD ["python","backend/app.py","run-server","--port","8000"]
