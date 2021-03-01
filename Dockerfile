# Set up the base image
FROM python:3.7-alpine
MAINTAINER Kshitij Singh

# Set up environment variable
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY DynamicProjectSchedulingApp/requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
     gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r ./requirements.txt
RUN apk del .tmp-build-deps


# Switch working directory
RUN mkdir /DynamicProjectSchedulingApp
WORKDIR /DynamicProjectSchedulingApp
COPY ./DynamicProjectSchedulingApp /DynamicProjectSchedulingApp

# Add a directory for storing images
# media - uploaded by user
# static - js, css, html, etc.
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# Switch to non root user(for security)
RUN adduser -D django_backend
RUN chown -R django_backend:django_backend /vol
RUN chmod -R 755 /vol/web
USER django_backend
