FROM python:3.12-alpine AS base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apk add --no-cache --virtual build-deps g++ libffi-dev

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
RUN apk del build-deps


FROM base AS runtime

# Install application into container
COPY . .

# Copy virtual env from python-deps stage
RUN rm -r /.venv
COPY --from=python-deps /.venv /.venv

# Run the application
ENTRYPOINT ["/.venv/bin/python", "src/main.py"]
