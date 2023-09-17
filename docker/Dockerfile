ARG SITENAME="django_starter"
ARG PYTHON_VERSION=3.11.5
ARG POETRY_VERSION=1.6.1
ARG POETRY_HOME=/home/ops/poetry

### STAGING

# pull official base image
FROM python:$PYTHON_VERSION-alpine AS staging
ARG POETRY_VERSION
ARG POETRY_HOME

# set environment variables
ENV POETRY_VERSION=$POETRY_VERSION
ENV POETRY_HOME=$POETRY_HOME

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
ARG POETRY_HOME

# set environment variables
ENV POETRY_VERSION=$POETRY_VERSION
ENV POETRY_HOME=$POETRY_HOME

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
ARG POETRY_HOME

# set environment variables
ENV POETRY_VERSION=$POETRY_VERSION
ENV POETRY_HOME=$POETRY_HOME

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
ARG POETRY_VERSION
ARG POETRY_HOME

# set environment variables
ENV SITENAME=$SITENAME
ENV POETRY_VERSION=$POETRY_VERSION
ENV POETRY_HOME=$POETRY_HOME

# set working directory
WORKDIR /home/ops/src

# install dependencies
COPY --from=build /home/ops/src/dist/*.whl ./
COPY --from=build /home/ops/src/constraints.txt ./
RUN pip install ./$SITENAME*.whl --constraint constraints.txt

# entrypoint
ENTRYPOINT ["../entrypoint.sh"]
CMD ["gunicorn", "--bind :$PORT", "--workers 1", "--threads 1", "--timeout 0", "\"$SITENAME:create_app()\""]
