FROM ubuntu:latest

RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
    echo "deb http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial main" >/etc/apt/sources.list && \
    echo "deb http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial-updates main" >>/etc/apt/sources.list && \
    echo "deb http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial universe" >>/etc/apt/sources.list && \
    echo "deb http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial-updates universe" >>/etc/apt/sources.list && \
    echo "deb http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial-security main" >>/etc/apt/sources.list && \
    echo "deb http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial-security universe" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial main" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial-updates main" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial universe" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial-updates universe" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial-security main" >>/etc/apt/sources.list && \
    echo "deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ xenial-security universe" >>/etc/apt/sources.list

RUN apt update && apt install -y python3-pip

RUN apt-get install -y libmysqlclient-dev

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

COPY . /usr/src/app/

EXPOSE 80

CMD ["python3", "./app.py"]

