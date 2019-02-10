FROM python:3.6
ADD . /songsapi
WORKDIR /songsapi
RUN pip install -r requirements.txt