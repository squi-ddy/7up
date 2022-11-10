FROM python:bullseye

WORKDIR /app/

RUN apt install cargo 
# a package requires this??? 

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
