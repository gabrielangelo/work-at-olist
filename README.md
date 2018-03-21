# Work at Olist

Implementation of [work-at-olist](https://github.com/olist/work-at-olist).
The repositry focus in the [problem](https://github.com/olist/work-at-olist/blob/3aca8ce2ef2cc66645fe864bc2128d55b10f6ee6/README.md) that has been changed to another [problem](https://github.com/olist/work-at-olist/blob/master/README.md).

## Main tools used in this project

* Ubuntu 16.04 LTS
* Pycharm CE 2017.1
* Python 3.5.2
* Django 1.11.3
* Django REST Framework 3.6.3


## Getting Started

### Prerequisites

* Python 3.5.2
* Postgres 9.3.15 (optional but recommended)


### Installing

1. Create an .env file and set variables. Examples can be found in `local.env`.

2. Create a virtual environment:

```
$ virtualenv <env_name>
$ source <env_name>/bin/activate
```

3. Install Python dependencies:

```
$ pip install -r requirements-local.txt
```

4. Run migrations:

```
$ python manage.py migrate
```

5. Start the server:

```
$ python manage.py runserver
```

The site will be available on <http://127.0.0.1:8000>.


## REST API

REST API docs can be found in <http://127.0.0.1:8000/api/v1/docs/> or https://work-at-olist-he.herokuapp.com.


## Deploy

To deploy to heroku:

1. Create a project in Heroku
2. Add a Postgres database
3. Set environment variables
4. Push to the Heroku repository:

```
$ git push heroku master
```

5. Run migrations:

```
$ heroku run python manage.py migrate
```

## Authors

* **Gabriel Angelo** - [gabrielangelo](https://github.com/gabrielangelo/)

