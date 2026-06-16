FROM docker.io/python:3-alpine

COPY ./requirements.txt /app/requirements.txt

RUN mkdir -p /app
WORKDIR /app
RUN chmod -R a+rwx /app

COPY app.py /app
COPY requirements.txt /app

RUN python3 -m pip install -r requirements.txt

# configure command to execute when container is run
CMD ["python3", "-m" , "flask", "--debug", "run", "--host=0.0.0.0"]

EXPOSE 5000
