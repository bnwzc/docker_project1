FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install Flask
RUN pip install Flask Flask-CORS
EXPOSE 5003
CMD ["python", "app.py"]
