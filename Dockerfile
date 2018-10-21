ARG DEPLOY_DIR=/opt/om-parser-stw-potsdam-v2
ARG LISTEN_PORT=3080

# Build & test container
FROM python:2.7-alpine as buildsys
ARG DEPLOY_DIR

# Install required dependencies
RUN apk add make
RUN pip install pipenv

# Add app user
RUN adduser -D flaskd

# Create app folder
RUN mkdir -p ${DEPLOY_DIR}
WORKDIR ${DEPLOY_DIR}

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

# Install environment
RUN pipenv install --two --dev

# Run tests
RUN make test


# Executable container

FROM python:2.7-alpine

ARG DEPLOY_DIR
ARG LISTEN_PORT

ENV LISTEN_PORT=$LISTEN_PORT
ENV LISTEN=0.0.0.0:$LISTEN_PORT

RUN apk add --no-cache uwsgi uwsgi-python
RUN pip install pipenv
RUN adduser -D flaskd

COPY --from=buildsys ${DEPLOY_DIR} ${DEPLOY_DIR}

WORKDIR ${DEPLOY_DIR}
RUN rm -rf ./tests ./Makefile
RUN chown -R flaskd:flaskd .

USER flaskd

ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install --two --deploy

EXPOSE $LISTEN_PORT
CMD pipenv run uwsgi --master --http11-socket $LISTEN --plugins python --protocol uwsgi --wsgi stw_potsdam.views:app --virtualenv ./.venv
