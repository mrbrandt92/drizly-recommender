FROM python:3.7-buster

RUN mkdir -p /usr/service/drizly_recommender
WORKDIR /usr/service/drizly_recommender
COPY requirements.txt .

RUN apt-get update
# RUN apt-get install no prompt
RUN apt-get install -y build-essential

RUN pip install --upgrade -r requirements.txt
COPY run_script.py .
COPY app.py .
COPY src src

EXPOSE 8080
EXPOSE 8081

CMD ["python","app.py"]
