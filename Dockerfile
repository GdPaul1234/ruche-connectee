FROM node:current-slim as front-build-stage

WORKDIR /tmp

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY ./frontend/package*.json ./

RUN npm ci

# Bundle app source
COPY ./frontend/ ./

# Build the typescript app
RUN npm run build


FROM python:3.11-slim as back-requirements-stage

WORKDIR /tmp

RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files to the /tmp directory.
COPY ./backend/pyproject.toml ./backend/poetry.lock* /tmp/

# Generate the requirements.txt file.
RUN poetry export -f requirements.txt --with api --with auth --with db  --output requirements.txt --without-hashes


FROM python:3.11-slim

# Copy builded frontend
WORKDIR /usr/src/frontend
COPY --from=front-build-stage /tmp/build ./build

WORKDIR /usr/src/backend

# Copy the requirements.txt file from back-requirements-stage and install it
COPY --from=back-requirements-stage /tmp/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./backend/env/docker.env env/prod.env
EXPOSE 80

# Run the backend, ready to serve the frontend
CMD ["python", "main.py"]
