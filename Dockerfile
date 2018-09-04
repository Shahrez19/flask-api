FROM ubuntu:latest

MAINTAINER Shahrez Jan "snjan19@bu.edu"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]