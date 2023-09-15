ARG SITENAME="django_starter"

ARG PYTHON_VERSION=3.11.5
ARG POETRY_VERSION=1.6.1
ARG SECRET_KEY=your_secret_key_here
ARG DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1]"

ARG SQL_DEV_DB=myproject_dev_db
ARG SQL_DEV_USER=django_db_user
ARG SQL_DEV_PASS=password
ARG SQL_DEV_HOST=myproject-db
ARG SQL_DEV_PORT=5432

ARG SQL_TEST_DB=myproject_test_db
ARG SQL_TEST_USER=django_db_user
ARG SQL_TEST_PASS=password
ARG SQL_TEST_HOST=myproject-db
ARG SQL_TEST_PORT=5432

ARG SQL_PROD_DB=myproject_db
ARG SQL_PROD_USER=django_db_user
ARG SQL_PROD_PASS=password
ARG SQL_PROD_HOST=myproject-db
ARG SQL_PROD_PORT=5432

### STAGING

# pull official base image
FROM python:$PYTHON_VERSION-alpine AS staging
ARG POETRY_VERSION

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV POETRY_HOME=/home/ops/poetry
ENV POETRY_VERSION=$POETRY_VERSION
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

# install linux dependencies
RUN apk update && apk upgrade && \
  apk add --no-cache gcc g++ musl-dev curl libffi-dev postgresql-dev zlib-dev jpeg-dev freetype-dev

# create and run as non-root user
RUN adduser --disabled-password ops
WORKDIR /home/ops

# install poetry to manage python dependencies
RUN curl -sSL https://install.python-poetry.org | python3 -

# import site
COPY ./docker/entrypoint.sh ./entrypoint.sh
COPY ./README.md ./README.md
COPY ./src ./src

# use non-root user
RUN chown -R ops:ops /home/ops
USER ops


### DEVELOPMENT

FROM staging AS dev
ARG POETRY_VERSION
ARG SECRET_KEY
ARG DJANGO_ALLOWED_HOSTS
ARG SQL_DEV_DB
ARG SQL_DEV_USER
ARG SQL_DEV_PASS
ARG SQL_DEV_HOST
ARG SQL_DEV_PORT

# set environment variables
ENV DEBUG=1
ENV SECRET_KEY=$SECRET_KEY
ENV DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS
ENV SQL_ENGINE=django.db.backends.postgresql
ENV SQL_DATABASE=$SQL_DEV_DB
ENV SQL_USER=$SQL_DEV_USER
ENV SQL_PASSWORD=$SQL_DEV_PASS
ENV SQL_HOST=$SQL_DEV_HOST
ENV SQL_PORT=$SQL_DEV_PORT
ENV DATABASE=postgres
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV POETRY_HOME=/home/ops/poetry
ENV POETRY_VERSION=$POETRY_VERSION
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

# set working directory
WORKDIR /home/ops/src

# install dependencies
ENV PATH="${PATH}:/home/ops/poetry/bin"
RUN poetry install --no-root

# run entrypoint
ENTRYPOINT ["../entrypoint.sh"]


### TEST

FROM staging AS test
ARG POETRY_VERSION
ARG SECRET_KEY
ARG DJANGO_ALLOWED_HOSTS
ARG SQL_TEST_DB
ARG SQL_TEST_USER
ARG SQL_TEST_PASS
ARG SQL_TEST_HOST
ARG SQL_TEST_PORT

# set environment variables
ENV DEBUG=1
ENV SECRET_KEY=$SECRET_KEY
ENV DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS
ENV SQL_ENGINE=django.db.backends.postgresql
ENV SQL_DATABASE=$SQL_TEST_DB
ENV SQL_USER=$SQL_TEST_USER
ENV SQL_PASSWORD=$SQL_TEST_PASS
ENV SQL_HOST=$SQL_TEST_HOST
ENV SQL_PORT=$SQL_TEST_PORT
ENV DATABASE=postgres
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV POETRY_HOME=/home/ops/poetry
ENV POETRY_VERSION=$POETRY_VERSION
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

# set working directory
WORKDIR /home/ops/src

# install dependencies
ENV PATH="${PATH}:/home/ops/poetry/bin"
RUN poetry install --no-root

# run entrypoint
RUN poetry run black .
RUN poetry run isort .
RUN poetry run flake8 .
RUN poetry run pytest
RUN poetry run pytest --cov=.


### BUILD

FROM staging AS build

# set working directory
WORKDIR /home/ops/src

# create wheels
ENV PATH="${PATH}:/home/ops/poetry/bin"
RUN poetry build --format wheel
RUN poetry export --format constraints.txt --output constraints.txt --without-hashes


### PRODUCTION

FROM build as prod
ARG SITENAME
ARG SECRET_KEY
ARG DJANGO_ALLOWED_HOSTS
ARG SQL_PROD_DB
ARG SQL_PROD_USER
ARG SQL_PROD_PASS
ARG SQL_PROD_HOST
ARG SQL_PROD_PORT

# set environment variables
ENV DEBUG=0
ENV SITENAME=$SITENAME
ENV SECRET_KEY=$SECRET_KEY
ENV DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS
ENV SQL_ENGINE=django.db.backends.postgresql
ENV SQL_DATABASE=$SQL_PROD_DB
ENV SQL_USER=$SQL_PROD_USER
ENV SQL_PASSWORD=$SQL_PROD_PASS
ENV SQL_HOST=$SQL_PROD_HOST
ENV SQL_PORT=$SQL_PROD_PORT
ENV DATABASE=postgres
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV PORT=8888

# set working directory
WORKDIR /home/ops/src

# install dependencies
COPY --from=build /home/ops/src/dist/*.whl ./
COPY --from=build /home/ops/src/constraints.txt ./
RUN pip install ./$SITENAME*.whl --constraint constraints.txt

# entrypoint
ENTRYPOINT ["../entrypoint.sh"]
CMD ["gunicorn", "--bind :$PORT", "--workers 1", "--threads 1", "--timeout 0", "\"$SITENAME:create_app()\""]
