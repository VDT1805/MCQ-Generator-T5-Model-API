# FROM alpine:latest
# RUN apk update
# RUN apk add py-pip
# RUN apk add --no-cache python3-dev 
# RUN pip install --upgrade --break-system-packages pip 
# ENV PIP_BREAK_SYSTEM_PACKAGES 1
# WORKDIR /app
# COPY . /app
# RUN pip --no-cache-dir install -r requirements.txt
# CMD ["python3", "app.py"]
FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "app.py"]