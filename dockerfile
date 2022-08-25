FROM python:3.9
WORKDIR /app
COPY ./app /app

RUN apt-get update
RUN apt-get install libgl1  -y
RUN pip install -r requirements.txt

EXPOSE 8000
CMD [ "gunicorn", "-k", "gevent", "server:app", "-b", "0.0.0.0:8000"]