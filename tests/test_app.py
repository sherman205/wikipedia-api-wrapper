"""
Tests for Flask routes in app.py
"""

import json
import wikipedia
from unittest.mock import patch
from app import app


def test_index_route():
	"""Test that index (/) endpoint returns 200 status and expected message."""
	expected_response_msg = 'Welcome to the Wikipedia API Flask App!'
	response = app.test_client().get('/')

	assert response.status_code == 200
	assert response.data.decode('utf-8') == expected_response_msg


@patch.object(wikipedia.wikipedia_api.WikipediaAPIWrapper, 'get_most_viewed_articles')
def test_get_most_viewed_articles(mock_get_most_viewed_articles):
	"""Test that /most_viewed_articles endpoint returns 200 status and appropriate json response."""
	mock_get_most_viewed_articles.return_value = [{'article': 'test'}]
	response = app.test_client().get('/most_viewed_articles')
	res = json.loads(response.data.decode('utf-8'))

	assert response.status_code == 200
	assert type(res[0]) is dict
	assert res[0]['article'] == 'test'


@patch.object(wikipedia.wikipedia_api.WikipediaAPIWrapper, 'get_article_view_count')
def test_get_article_view_count(mock_get_article_view_count):
	"""Test that /article_view_count endpoint returns 200 status and appropriate json response."""
	article_title = 'test'
	article_view_count = 2000
	mock_get_article_view_count.return_value = article_view_count
	response = app.test_client().get(f'/article_view_count/{article_title}')
	res = json.loads(response.data.decode('utf-8'))

	assert response.status_code == 200
	assert type(res) is dict
	assert res['article'] == article_title
	assert res['view_count'] == article_view_count


@patch.object(wikipedia.wikipedia_api.WikipediaAPIWrapper, 'get_day_with_most_views')
def test_get_most_views_day(mock_get_day_with_most_views):
	"""Test that /most_views_day endpoint returns 200 status and appropriate json response."""
	article_title = 'test'
	most_views_date = '01/01/2023'
	mock_get_day_with_most_views.return_value = most_views_date
	response = app.test_client().get(f'/most_views_day/{article_title}')
	res = json.loads(response.data.decode('utf-8'))

	assert response.status_code == 200
	assert type(res) is dict
	assert res['article'] == article_title
	assert res['most_views_day'] == most_views_date
