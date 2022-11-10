FROM python:bullseye

WORKDIR /app/

RUN apt update
RUN apt install -y cargo 
# a package requires this??? 

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
