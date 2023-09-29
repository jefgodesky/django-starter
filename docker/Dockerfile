ARG SITENAME="django_starter"
ARG PYTHON_VERSION=3.11.5

### STAGING

# pull official base image
FROM python:$PYTHON_VERSION-alpine AS staging

# install linux dependencies
RUN apk update && apk upgrade && \
  apk add --no-cache gcc g++ musl-dev curl libffi-dev postgresql-dev zlib-dev jpeg-dev freetype-dev

# create and run as non-root user
RUN adduser --disabled-password ops
WORKDIR /home/ops

# import site
COPY ./docker/entrypoint.sh ./entrypoint.sh
COPY ./README.md ./README.md
COPY ./src ./src

# use non-root user
RUN chown -R ops:ops /home/ops
USER ops


### DEVELOPMENT

FROM staging AS dev

# set working directory
WORKDIR /home/ops/src

# install dependencies
COPY ./src/requirements.dev.txt ./requirements.dev.txt
RUN pip install -r requirements.dev.txt

# run entrypoint
ENTRYPOINT ["../entrypoint.sh"]


### TEST

FROM staging AS test

# set working directory
WORKDIR /home/ops/src

# install dependencies
COPY ./src/requirements.dev.txt ./requirements.dev.txt
RUN pip install -r requirements.dev.txt

# run entrypoint
RUN black .
RUN isort .
RUN flake8 .
RUN pytest
RUN pytest --cov=.


### PRODUCTION

FROM staging as prod
ARG SITENAME

# set environment variables
ENV SITENAME=$SITENAME

# set working directory
WORKDIR /home/ops/src

# install dependencies
COPY ./src/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# entrypoint
ENTRYPOINT ["../entrypoint.sh"]
CMD ["gunicorn", "--bind :$PORT", "--workers 1", "--threads 1", "--timeout 0", "\"$SITENAME:create_app()\""]
