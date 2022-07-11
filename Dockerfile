FROM python:bullseye

WORKDIR /app/
COPY . .
RUN pip install -r requirements.txt