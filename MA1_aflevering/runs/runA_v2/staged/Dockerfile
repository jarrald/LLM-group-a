FROM python:3.12-slim
WORKDIR /app
COPY src /app/src
RUN python -m pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "taskflow"]
EXPOSE 8080
