FROM python:3.7.9
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run" , "--host", "0.0.0.0"]

# more performant solution than flask built in development server
# we had CMD ["flask", "run" , "--host", "0.0.0.0"]\
# but for deploying for render better use gunicorn (uwsgi - is deprecated)