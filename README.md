## Synopsis

Sneaker Shelf web application for keeping track of your favorite sneakers.

## Website
http://www.kennedyfamilyrecipes.com

## What Does This Tool Do?
Keeps track of all your sneakers.

## How to Run (Development)

1. Create the Dockerfile for the postgres service

- % cd ./sneaker_project/web/
- % python create_postgres_dockerfile.py
- % cd ..

2. Build and run the Docker containers

- % docker-compose build
- % docker-compose up -d

3. Create or re-initialize the database

- % docker-compose run --rm web python ./instance/db_create.py

Go to your favorite web browser and open:
    localhost:80

## Key Python Modules Used

- Flask - web framework
- Jinga2 - templating engine
- SQLAlchemy - ORM (Object Relational Mapper)
- Flask-Bcrypt - password hashing
- Flask-Login - support for user management
- Flask-Migrate - database migrations
- Flask-WTF - simplifies forms
- itsdangerous - helps with user management, especially tokens

This application is written using Python 3.8.0.  The database used is PostgreSQL.

Docker is the recommended tool for running in development and production.

## Unit Testing

In the top-level folder:
    % nose2
