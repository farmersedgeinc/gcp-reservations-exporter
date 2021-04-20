FROM python:3.7-alpine

WORKDIR /usr/src/app
RUN adduser -D -u 25000 -g app -h /usr/src/app app && \
    chown app:app /usr/src/app

RUN apk add tzdata
RUN apk add curl
RUN apk add bash
RUN curl -sSL https://sdk.cloud.google.com > /tmp/gcl && bash /tmp/gcl --install-dir=./gcloud --disable-prompts
# RUN source /usr/src/app/gcloud/google-cloud-sdk/path.bash.inc

EXPOSE 8003

RUN pip install --no-cache-dir pipenv
COPY Pipfile* ./
RUN pipenv install --system --deploy

COPY exporter.py ./
# COPY setup.cfg ./

USER app
CMD [ "python", "-u", "./exporter.py" ]
