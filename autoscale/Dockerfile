FROM python:3.5
MAINTAINER Guerreiro Maxime <docker@docbleach.xyz>

WORKDIR /app/
COPY . /app/

RUN pip3 install -r requirements.txt

CMD ["/app/entrypoint.sh"]