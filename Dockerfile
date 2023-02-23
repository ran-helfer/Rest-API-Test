FROM python:3.7.9
# EXPOSE 5000 - gunicorn is running on port 80
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --updrade -r requirements.txt
COPY . .
# CMD ["flask", "run" , "--host", "0.0.0.0"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]

# more performant solution than flask built in development server
# we had CMD ["flask", "run" , "--host", "0.0.0.0"]\
# but for deploying for render better use gunicorn (uwsgi - is deprecated)