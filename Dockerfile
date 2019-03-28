FROM python:latest

# We copy this file first to leverage docker cache
COPY ./requirements.txt /code/pycode/requirements.txt

WORKDIR /code/pycode

RUN pip install -r requirements.txt

COPY . /code/pycode

RUN python setup.py bdist_wheel

