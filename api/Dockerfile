FROM python:3.5-alpine

EXPOSE 5000
HEALTHCHECK CMD curl --fail http://localhost:5000/ping

ENV INTERNAL_PLIK_SERVER https://plik.root.gg

# We add the Plik binary file
ADD https://plik.root.gg/clients/linux-amd64/plik /usr/bin/plik

RUN apk add -t build --no-cache --update-cache \
    # Having up to date SSL certificates is always a good thing. :)
    ca-certificates \
    openssl \
    # For the healthcheck
    curl \
    && \
    update-ca-certificates && \

    # Add glibc, wanted by plik (compiled with Go)
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.23-r3/glibc-2.23-r3.apk && \
    apk add glibc-2.23-r3.apk && \

    # Remove openssl, only needed for wget
    apk del build wget unzip && \

    # We add an user
    adduser -S -u 1000 worker && \

    # Add default config for Plik, required
    chmod o+x /usr/bin/plik && \
    echo 'URL = "https://plik.root.gg"' > /home/worker/.plikrc


# Install the python dependencies
ADD requirements.txt /app/
WORKDIR /app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app/
RUN chown -R worker /app/; chmod -R 770 /app/

USER worker
ENTRYPOINT ["python3", "/app/docbleach.py"]
