FROM python:3
WORKDIR /app/
COPY src /app/
RUN ls -l
RUN pip install -r requirements.txt
