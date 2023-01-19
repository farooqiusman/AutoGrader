FROM python:3.9.8
ADD . /AutoGrader
WORKDIR /AutoGrader
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
EXPOSE 5960
EXPOSE 5000
CMD python3 run.py prod
