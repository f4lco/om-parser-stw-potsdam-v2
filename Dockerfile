# Build & test container
FROM python:2.7-alpine as buildsys

# Install required dependencies
RUN apk add make
RUN pip install pipenv

# Add app user
RUN adduser -D flaskd

# Create app folder
RUN mkdir -p /opt/om-parser-stw-potsdam-v2
WORKDIR /opt/om-parser-stw-potsdam-v2

# Copy app folder contents
COPY stw_potsdam/ ./stw_potsdam
COPY tests ./tests
COPY Makefile .
COPY Pipfile .
COPY Pipfile.lock .

# Apply app user to app folder
RUN chown -R flaskd:flaskd .

# Prepare environment
USER flaskd
ENV PYTHONPATH="/opt/om-parser-stw-potsdam-v2:${PYTHONPATH}"

# Install environment
RUN pipenv install --two --dev

# Run tests
RUN make test


# Executable container

FROM python:2.7-alpine

RUN apk add uwsgi uwsgi-python
RUN pip install pipenv
RUN adduser -D flaskd

RUN mkdir -p /opt/om-parser-stw-potsdam-v2
COPY --from=buildsys /opt/om-parser-stw-potsdam-v2 /opt/om-parser-stw-potsdam-v2

WORKDIR /opt/om-parser-stw-potsdam-v2
RUN chown -R flaskd:flaskd .

USER flaskd
ENV PYTHONPATH="/opt/om-parser-stw-potsdam-v2:${PYTHONPATH}"

ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install --two --deploy

EXPOSE 3080
CMD [ "pipenv", "run", "uwsgi", "--master", "--http11-socket", "0.0.0.0:3080", "--plugins", "python", "--protocol", "uwsgi", "--wsgi", "stw_potsdam.views:app", "--virtualenv", "./.venv" ]
