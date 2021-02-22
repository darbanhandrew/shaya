# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN apk update \
    && apk add --virtual build-deps gcc rust cargo libffi-dev openssl-dev libressl-dev python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && pip install -r requirements.txt \
    && apk del build-deps


# copy entrypoint.sh
#COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]