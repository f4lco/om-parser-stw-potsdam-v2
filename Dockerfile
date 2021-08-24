ARG DEPLOY_DIR=/opt/om-parser-stw-potsdam-v2
ARG USERNAME=flaskd
ARG LISTEN_PORT=3080


### Shared base container
FROM python:3.8-alpine as basesys
ARG DEPLOY_DIR
ARG USERNAME

# Install dependencies
RUN pip install pipenv

# Add app user
RUN adduser -D ${USERNAME}

# Create app folder
RUN mkdir -p ${DEPLOY_DIR}

# Enable local venv
ENV PIPENV_VENV_IN_PROJECT=1

# Switch to app folder
WORKDIR ${DEPLOY_DIR}

# Copy app folder contents
COPY stw_potsdam/ ./stw_potsdam
COPY tests ./tests
COPY Makefile .
COPY Pipfile .
COPY Pipfile.lock .

# Apply app user to app folder
RUN chown -R ${USERNAME} .

# Prepare environment
USER ${USERNAME}


### Build & test container
FROM basesys as buildsys
ARG DEPLOY_DIR
ARG USERNAME

# Install required build dependencies
USER root
RUN apk add make gcc musl-dev linux-headers python3-dev

# Install environment
USER ${USERNAME}
RUN pipenv install --dev

# Run tests
RUN make test

# Clean up test environment
RUN rm -rf .venv
RUN rm -rf ./tests ./Makefile

# Install production environment
RUN pipenv install --deploy


### Production container

FROM basesys
ARG DEPLOY_DIR
ARG LISTEN_PORT
ARG USERNAME

# Install dependencies
USER root
RUN apk add curl

# Copy built app
USER ${USERNAME}
COPY --from=buildsys ${DEPLOY_DIR}/.venv ${DEPLOY_DIR}/.venv
WORKDIR ${DEPLOY_DIR}

# Prepare runtime environment variables
ENV LISTEN_PORT=${LISTEN_PORT}
ENV LISTEN=0.0.0.0:${LISTEN_PORT}

EXPOSE ${LISTEN_PORT}
CMD pipenv run uwsgi --master --http11-socket $LISTEN --plugins python --protocol uwsgi --wsgi stw_potsdam.views:app --virtualenv ./.venv

HEALTHCHECK --interval=15s --timeout=3s CMD curl -f http://127.0.0.1:$LISTEN_PORT/health_check || exit 1
