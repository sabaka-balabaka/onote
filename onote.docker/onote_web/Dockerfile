FROM python:3

EXPOSE 5000

RUN mkdir /app.init
WORKDIR /app.init
COPY requirements.txt /app.init/requirements.txt
COPY setup.py /app.init/setup.py

RUN pip install -r requirements.txt
RUN python setup.py
