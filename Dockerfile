FROM python:3.7.4

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN pip install -U pip

# six is required to be installed before `awssig`
# https://github.com/dacut/python-aws-sig/issues/2
RUN pip install six
RUN pip install -r requirements.txt

ADD . /app/
