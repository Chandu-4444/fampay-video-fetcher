# fampay-video-fetcher

A youtube videos fetcher written in Python's Django Restframework. The following lines describe the structure of the application:

- Contains an asynchronous celery beat scheduled task that runs every 10 seconds. This fetches the youtube data v3 api for the videos based on the query provides in the .env file. The results are saved to the database.
- We can get the fetched results through `/api/fetch/?page=<PAGE NUMBER>`.
- We can search for a different query in the fetched results through `/api/search/?page=<PAGE NUMBER>&query=<SEARCH QUERY>`.

## Steps to run the project

### Through Docker

Make sure you have docker and docker-compose installed and are working correctly for this step.
Before running the `docker-compose build`, we need to configure the docker.env file so that the containers use the correct environment variables. The docker.env file is of the same format as the env.format file and is contained in the root folder of the project where `manage.py` exists. My docker.env file is as follows:

```bash
# docker.env file

export DEBUG=1

export DB_NAME=postgres
export DB_USER=postgres
export DB_PASS=postgres
export DB_SERVICE=pgdb
export DB_PORT=5432

export REDIS_HOST=redis

export POSTGRES_DB=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres

export API_KEY="space seperated youtube api keys"
export SEARCH_QUERY='cricket'
export OAUTHLIB_INSECURE_TRANSPORT=1

```

```bash
docker-compose build
docker-compose up
```

This should start the application and the celery beat as docker containers.

### Running the project locally

For this we need to run the following steps:

```bash
sudo apt install virtualenv
sudo pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib redis
```

Use the env.format file to create a .env file with correct values:

```bash
# .env file

export DEBUG=1

export DB_NAME=fampay
export DB_USER=fampay_user
export DB_PASS=fampay_user_password
export DB_SERVICE=localhost
export DB_PORT=5432

export REDIS_HOST=localhost

export API_KEY="space seperated youtube api keys"
export SEARCH_QUERY='cricket'
export OAUTHLIB_INSECURE_TRANSPORT=1
```

We'll now setup the database:

```bash
bash> source .env
bash> sudo -u postgres psql

postgres> CREATE DATABASE $DB_NAME;
postgres> CREATE USER $DB_USER WITH PASSWORD $DB_PASS;
postgres> ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
postgres> ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
postgres> ALTER ROLE $DB_USER SET timezone TO 'UTC';
postgres> GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
postgres> \q
```

Now we're ready to launch the project.

```bash
# Django project

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Run the celery task in a seperate terminal
celery -A fampay worker -B -l DEBUG -P threads
```

If everything goes well, we can hit the respective APIs.


