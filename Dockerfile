FROM python:3.9.8
ADD . /AutoGrader
WORKDIR /AutoGrader
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN apt-get update && apt-get -y install openjdk-11-jdk-headless 
EXPOSE 5960
EXPOSE 5000
CMD python3 run.py prod

