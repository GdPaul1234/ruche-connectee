# Ruche connectée

![image](https://user-images.githubusercontent.com/61539971/222790917-704af435-f8a4-4753-9da1-053350a038ef.png)

A web application to retrieve data from sensors in the hives built with FastApi, React and MongoDB

## Installation

Prerequisite: a running MongoDB server with at least one replica set node.
The replica set is required  for transactions.

### Backend installation

Poetry, the python dependency manager that we used will create a virtual environment
and install all dependencies automatically on the first run.

To install Poetry, follow the instructions given in
the [official documentation](https://python-poetry.org/docs/#installation).

This project needs at least Python 3.10

### Configuring the backend

To configure properly the application: create a `prod.env` and/or `test.env` files in the `/backend/env folder`.

Here a example:

```env
DEBUG_MODE=True
DB_URL="mongodb://localhost:27017/"
DB_NAME="ruche-connectee"

SECRET_KEY="alongsuiteofrandomcharacters"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The dotenv file is validated by Pydandic on runtime according to the this [file](./backend/config/__init__.py).

### Frontend installation

Node is required for building the frontend part.

To install the required dependencies (React...), run `npm install` in the `frontend` directory.

Before running the app in the development mode with `npm run start` or building it (`npm run build`),
you must generate the OpenApi client from the OpenAPI located on `http://adress-of-backend/openapi.json`.

A ready-to-use npm script is provided: just run `npm run build-api-client` after ensuring that the
backend is running and properly configured.

## Usage

To run the backend:

```sh
cd backend
poetry run main.py
```

To run the frontend in development mode:

```sh
cd frontend
npm run start
```

and open [http://localhost:3000](http://localhost:3000) to view it in the browser.

Finally, to run tests: run `pytest` in the backend folder.

A ready to be used `docker-compose.yml` is provided for convenience.

## Release note

You can find the release note [here](./RELEASE_NOTE.md).
