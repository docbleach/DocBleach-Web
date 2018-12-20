FROM openjdk:8-jre-alpine

ENTRYPOINT ["/app/entrypoint.sh"]

HEALTHCHECK CMD /usr/bin/celery inspect ping -A docbleach.tasks -d celery@$HOSTNAME

ENV FINAL_PLIK_SERVER https://plik.root.gg

# Stored on Plik for now, as we don't yet have the GitHub Link
ENV DOCBLEACH_JAR https://github.com/docbleach/DocBleach/releases/download/v0.0.9/docbleach.jar

# We add the Plik binary file
ADD https://plik.root.gg/clients/linux-amd64/plik /usr/bin/plik

RUN apk add --no-cache --update-cache \
    # Having up to date SSL certificates is always a good thing. :)
    ca-certificates \
    openssl \
    python3 \
    && \
    update-ca-certificates && \

    # Add glibc, wanted by plik (compiled with Go)
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.23-r3/glibc-2.23-r3.apk && \
    apk add glibc-2.23-r3.apk && \

    # Setup Python 3
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    # Remove openssl, only needed for wget
    apk del openssl wget unzip && \

    # We add an user
    adduser -S -u 1000 worker && \

    # Add default config for Plik, required
    chmod o+x /usr/bin/plik && \
    echo 'URL = "https://plik.root.gg"' > /home/worker/.plikrc

# Install the celery dependency
ADD requirements.txt ${DOCBLEACH_JAR} /app/

WORKDIR /app/

RUN pip3 install --no-cache-dir -r requirements.txt && \
    chown -R worker /app/; chmod -R 770 /app/

USER worker
COPY . /app/
