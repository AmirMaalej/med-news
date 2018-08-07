# med-news

This project is for managing Articles and Authors for medical and health news.
Using Django 2.0, a postgres database with docker and docker-compose configuration files.

## Features:

  - APIs for storing and managing Articles and Authors.
  - get/list requests to Articles are cached with Memcached backend (WIP).
  - A GET parameter allows to filter the list of articles by a word that is contained in the body.
  - For every article listed, the author content is inlined.
  - In order to update/create an article, an inline author may be specified (which will be created) or the id of an already existing author.
  - Deleting an author should delete all related articles.

## Requirements:

  - docker
  - docker compose

## Run with:

    $ docker-compose up

Run migrations and create superusers inside the running container.

    $ docker exec -it mednews_web_1 python3 manage.py migrate
    $ docker exec -it mednews_web_1 python3 manage.py createsuperuser --username admin

You can use swagger for API testing: http://localhost:8000/api/docs/