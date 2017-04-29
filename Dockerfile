FROM ubuntu:latest

RUN apt update && apt install -y python3-pip

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install -r requirements.txt

COPY . /usr/src/app/

EXPOSE 80

CMD ["python3", "./app.py"]
