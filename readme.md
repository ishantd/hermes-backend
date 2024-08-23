<h1 align="center">hermes</h1>

The hermes Backend.

## Local Quickstart (MacOS)

The fastest way to get the hermes backend set up locally.

### 1. Install dependencies (MacOS)


Create a new miniconda environment.

```shell
conda create -n hermes python=3.10
conda activate hermes
```


```shell
pip install -r requirements.txt requirements-dev.txt
```


⚠️ **remember to activate the conda environment:**

```shell
conda activate hermes
```

### 2. Set up database

First, create your database.

```shell
createdb hermes
```

Then, create your `.env` file. Make sure to set `DB_USER` and `DB_PASSWORD` to the values on your machine.

```
DB_HOST=localhost
DB_NAME=hermes
DB_PORT=5432
DB_USER=<YOUR DB USERNAME>
DB_PASSWORD=<YOUR DB PASSWORD>
```

Now if you want to use OpenAI API, you need to set the `OPENAI_API_KEY` in the `.env` file.

```shell
echo "OPENAI_API_KEY=<YOUR OPENAI API KEY>" >> .env
```

Now, let's get our database up to speed. Run all migrations with this command:

```shell
alembic upgrade head
```


### 2. Run application

You're set to run the app! Make sure you're in the root directory of the project, and run:

```shell
uvicorn app.api.app:get_app --factory --reload
```

Open API endpoint: `http://localhost:8000/api/docs`

Redoc endpoint: `http://localhost:8000/redoc`


### Running tests

To run unit tests locally:

```bash
ENV=TESTING pytest -vv .
```
