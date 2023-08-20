# Wikipedia API Wrapper

A Python Flask wrapper around the Wikipedia API to get information about wikipedia articles.

## Endpoints

All endpoints use query parameters to filter. If an invalid query parameter is used, it is ignored. If values for year or month are not specified, default values will be used. (year=2023, month=1).<br />
A json response is returned for successful data returns.<br />
If there is an error that happens either from querying the Wikipedia API or an application error, an Exception is thrown and an error is displayed.

### `GET /most_viewed_articles`

Gets a list of the top 1000 most viewed articles for a week or a month.

#### Usage:

- Most viewed articles for January 2020: `/most_viewed_articles?year=2020`
- Most viewed articles for April 2020: `/most_viewed_articles?year=2020&month=4`
- Most viewed articles for April 5, 2020: `/most_viewed_articles?year=2020&month=4&day=5`
- Most viewed articles for the week of April 4, 2020 - April 11, 2020: `/most_viewed_articles?year=2020&month=4&start_day=4&end_day=11`

### `GET /article_view_count/<article_title>`

Gets the view count of a specific article for a week or a month.

#### Usage:

- Article view count for January 2020: `/article_view_count/Main_Page?year=2020`
- Article view count for April 2020: `/article_view_count/Main_Page?year=2020&month=4`
- Article view count for the week of April 4, 2020 - April 11, 2020: `/article_view_count/Main_Page?year=2020&month=4&start_day=4&end_day=11`

### `GET /most_views_day/<article_title>`

Gets the day of the month when an article got the most page views. No date range is supported.

#### Usage:

- Date with the most views for January 2020: `/most_views_day/Main_Page?year=2020`
- Date with the most views for April 2020: `/most_views_day/Main_Page?year=2020&month=4`

## How to run

1. Clone this repo and navigate to that directory

#### Docker

Using port 8080 for docker

1. Install and setup [docker](https://docs.docker.com/get-docker/)
2. In the CLI, run `docker compose up --build`
3. Go to a browser: `http://127.0.0.1:8080/` to view the application

#### Native env

Using port 8000 if just running flask app without docker

(You can also spin up a python environment: [pyenv](https://github.com/pyenv/pyenv)) before proceeding:

1. In the CLI, run `pip install -r requirements.txt`
2. And then run `flask run --host 0.0.0.0 --port 8000`
3. Go to a browser: `http://127.0.0.1:8000/` to view the application

## Running tests

The tests are run as part of the Docker image creation when running `docker compose`.<br />
If a test fails, the execution of image creation and spinning up the container stops.

In the CLI, run `pytest`.

