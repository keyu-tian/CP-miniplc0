FROM python:3
WORKDIR /app/
COPY src /app/
RUN pip install -r src/requirements.txt
