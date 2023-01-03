# Albatross

This is a CMS for the [Pelican](https://blog.getpelican.com/) static site generator. It is a web-based application built with [FastAPI](https://fastapi.tiangolo.com/) and [Jinja](https://jinja.palletsprojects.com/).

*Note*: This is experimental as I am developing this with the help of ChatGPT.

## Features

- Create, read, update, and delete (CRUD) posts
- Automatic summary generation for posts
- Optional image for posts
- Author CRUD

## Requirements

- Python 3.10 or higher
- Pelican
- FastAPI
- Jinja
- SQLAlchemy
- Pygments

## Development setup

1. Clone the repository
2. Create a virtual environment: `python -m venv env`
3. Activate the virtual environment: `source env/bin/activate`
4. Install the dependencies:
    1. `make setup` (for the requirements to run the project)
    2. `make setup-dev` (for the development requirements)
5. Set the following environment variables:
   - `DATABASE_URI`: URI for the database
   - `APP_SECRET_KEY`: Secret key for the app
6. Run the development server: `make serve`

## Testing

Run the tests with: `make test`

## Linting and formatting

Run the linters with: `make lint`

Run the formatter with: `make format`

## Code coverage

Run the code coverage with: `make coverage`

## Makefile

- `make run`: Run the development server
- `make test`: Run the tests
- `make lint`: Run the linters
- `make format`: Run the formatter
- `make coverage`: Run the code coverage
- `make clean`: Clean up Python-related artifacts
- `make help`: Print a helpful message about how to use the Makefile
