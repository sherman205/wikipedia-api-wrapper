"""
Tests for logic in wikipedia_api.py
"""
import pytest
from unittest.mock import patch
from wikipedia.wikipedia_api import WikipediaAPIWrapper


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_most_viewed_articles(mock_get_articles_request):
    """
    Tests that calling get_most_viewed_articles() with year and month
    forms the correct Wikipedia API url endpoint and returns the expected data.
    """
    year = 2020
    month = 3
    mock_get_articles_request.return_value = [
        {'articles': [{'article': 'test1'}, {'article': 'test2'}]}
    ]
    articles = WikipediaAPIWrapper().get_most_viewed_articles(year, month)

    expected_url = f"top/en.wikipedia/all-access/{year}/{month:02d}/all-days"
    mock_get_articles_request.assert_called_with(expected_url)
    assert len(articles) == 2
    assert articles == [{'article': 'test1'}, {'article': 'test2'}]


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_most_viewed_articles_for_day(mock_get_articles_request):
    """
    Tests that calling get_most_viewed_articles() with year, month, and day
    forms the correct Wikipedia API url endpoint and returns the expected data.
    """
    year = 2020
    month = 3
    day = 20

    mock_get_articles_request.return_value = [
        {'articles': [{'article': 'test1'}, {'article': 'test2'}]}
    ]

    articles = WikipediaAPIWrapper().get_most_viewed_articles(year, month, day=day)

    expected_url = f"top/en.wikipedia/all-access/{year}/{month:02d}/{day:02d}"
    mock_get_articles_request.assert_called_with(expected_url)
    assert len(articles) == 2
    assert articles == [{'article': 'test1'}, {'article': 'test2'}]


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_most_viewed_articles_for_range(mock_get_articles_request):
    """
    Tests that calling get_most_viewed_articles() with year, month, start_day, and end_day
    forms the correct Wikipedia API url endpoint, makes the correct amount
    of calls, and returns the expected data.
    """
    year = 2020
    month = 3
    start_day = 4
    end_day = 5

    mock_get_articles_request.side_effect = [
        [{'articles': [{'article': 'test1', 'views': 300}, {'article': 'test2', 'views': 200}]}],
        [{'articles': [{'article': 'test2', 'views': 400}, {'article': 'test3', 'views': 100}]}]
    ]

    articles = WikipediaAPIWrapper().get_most_viewed_articles(year, month, start_day=start_day, end_day=end_day)

    assert mock_get_articles_request.call_count == 2
    assert len(articles) == 3
    assert articles == [{'article': 'test1', 'views': 300},
                        {'article': 'test2', 'views': 600},
                        {'article': 'test3', 'views': 100}]


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_most_viewed_articles_exception(mock_get_articles_request):
    """
    Tests that when calling get_most_viewed_articles() with year and month
    and the Wikipedia API throws an error, an exception is raised up.
    """
    year = 2020
    month = 3

    mock_get_articles_request.side_effect = Exception('mocked error')

    with pytest.raises(Exception) as e:
        WikipediaAPIWrapper().get_most_viewed_articles(year, month)

    expected_url = f"top/en.wikipedia/all-access/{year}/{month:02d}/all-days"
    mock_get_articles_request.assert_called_with(expected_url)
    assert str(e.value) == 'mocked error'


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_most_viewed_articles_range_user_error(mock_get_articles_request):
    """
    Tests that when calling get_most_viewed_articles() with year, month
    as well as start_day and end_day, but the start_day > end_day, an exception is raised up.
    """
    year = 2020
    month = 3
    start_day = 12
    end_day = 7

    with pytest.raises(Exception) as e:
        WikipediaAPIWrapper().get_most_viewed_articles(year, month, start_day=start_day, end_day=end_day)

    mock_get_articles_request.assert_not_called()
    assert str(e.value) == 'End date cannot be smaller than start date'


@patch.object(WikipediaAPIWrapper, '_get_articles_request', return_value=[])
def test_get_most_viewed_articles_no_articles_returned(mock_get_articles_request):
    """
    Tests that when calling get_most_viewed_articles() with year, month
    and the Wikipedia API returns an empty list of no article data, assert
    that an empty list is returned.
    """
    year = 2020
    month = 3

    articles = WikipediaAPIWrapper().get_most_viewed_articles(year, month)

    expected_url = f"top/en.wikipedia/all-access/{year}/{month:02d}/all-days"
    mock_get_articles_request.assert_called_with(expected_url)
    assert len(articles) == 0


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_article_view_count(mock_get_articles_request):
    """
    Tests that calling get_article_view_count() with article title, year, and month
    forms the correct Wikipedia API url endpoint and returns the correct view count.
    """
    article_title = "test1"
    year = 2020
    month = 3
    start = f'{year}{month:02d}01'
    end = f'{year}{month:02d}31'

    mock_get_articles_request.return_value = [
        {'article': 'test1', 'views': 300},
        {'article': 'test2', 'views': 200}
    ]

    view_count = WikipediaAPIWrapper().get_article_view_count(article_title, year, month)

    expected_url = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"
    mock_get_articles_request.assert_called_with(expected_url)
    assert view_count == 300


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_article_view_count_for_range(mock_get_articles_request):
    """
    Tests that calling get_article_view_count() with article title, year, month, start_day, and end_day
    forms the correct Wikipedia API url endpoint and returns the correct view count.
    """
    article_title = "test1"
    year = 2020
    month = 3
    start_day = 10
    end_day = 5
    start = f'{year}{month:02d}{start_day:02d}'
    end = f'{year}{month:02d}{end_day:02d}'

    mock_get_articles_request.return_value = [
        {'article': 'test1', 'views': 300},
        {'article': 'test1', 'views': 200}
    ]

    view_count = WikipediaAPIWrapper().get_article_view_count(article_title, year, month,
                                                              start_day=start_day, end_day=end_day)

    expected_url = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"
    mock_get_articles_request.assert_called_with(expected_url)
    assert view_count == 500


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_article_view_count_for_range_user_error(mock_get_articles_request):
    """
    Tests that calling get_article_view_count() with article title, year, month,
    as well as start_day and end_day, but the start_day > end_day, an exception is raised up.
    """
    article_title = "test1"
    year = 2020
    month = 3
    start_day = 5
    end_day = 10
    start = f'{year}{month:02d}{start_day:02d}'
    end = f'{year}{month:02d}{end_day:02d}'

    mock_get_articles_request.side_effect = Exception('mocked error')

    with pytest.raises(Exception) as e:
        WikipediaAPIWrapper().get_article_view_count(article_title, year, month,
                                                     start_day=start_day, end_day=end_day)

    expected_url = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"
    mock_get_articles_request.assert_called_with(expected_url)
    assert str(e.value) == 'mocked error'


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_article_view_count_month_user_error(mock_get_articles_request):
    """
    Tests that calling get_article_view_count() with article title, year and
    a bad month value
    forms the correct Wikipedia API url endpoint and returns the expected data.
    """
    article_title = "test1"
    year = 2020
    month = 0

    with pytest.raises(Exception) as e:
        WikipediaAPIWrapper().get_article_view_count(article_title, year, month)

    mock_get_articles_request.assert_not_called()
    assert str(e.value) == 'bad month number 0; must be 1-12'


@patch.object(WikipediaAPIWrapper, '_get_articles_request', return_value=[])
def test_get_article_view_count_no_response(mock_get_articles_request):
    """
    Tests that when calling get_article_view_count() with article title, year, and month
    and the Wikipedia API returns with no data, then the view count returned is 0.
    """
    article_title = "test1"
    year = 2020
    month = 3
    start = f'{year}{month:02d}01'
    end = f'{year}{month:02d}31'

    view_count = WikipediaAPIWrapper().get_article_view_count(article_title, year, month)

    expected_url = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"
    mock_get_articles_request.assert_called_with(expected_url)
    assert view_count == 0


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_day_with_most_views(mock_get_articles_request):
    """
    Tests that calling get_day_with_most_views() with article title, year, and month
    forms the correct Wikipedia API url endpoint and returns the stringified date.
    """
    article_title = "test1"
    year = 2020
    month = 3
    start = f'{year}{month:02d}01'
    end = f'{year}{month:02d}31'

    mock_get_articles_request.return_value = [
        {'article': 'test1', 'views': 300, 'timestamp': "2020030500"},
        {'article': 'test1', 'views': 200, 'timestamp': "2020032000"},
        {'article': 'test1', 'views': 700, 'timestamp': "2020031900"}
    ]

    date = WikipediaAPIWrapper().get_day_with_most_views(article_title, year, month)

    expected_url = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"
    mock_get_articles_request.assert_called_with(expected_url)
    assert date == '03/19/2020'


@patch.object(WikipediaAPIWrapper, '_get_articles_request')
def test_get_day_with_most_views_exception(mock_get_articles_request):
    """
    Tests that when calling get_day_with_most_views() with article title, year, and month
    and the Wikipedia API throws an error, an exception is raised up.
    """
    article_title = "test1"
    year = 2020
    month = 3
    start = f'{year}{month:02d}01'
    end = f'{year}{month:02d}31'

    mock_get_articles_request.side_effect = Exception('mocked error')

    with pytest.raises(Exception) as e:
        WikipediaAPIWrapper().get_day_with_most_views(article_title, year, month)

    expected_url = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"
    mock_get_articles_request.assert_called_with(expected_url)
    assert str(e.value) == 'mocked error'


@patch.object(WikipediaAPIWrapper, '_get_articles_request', return_value=[])
def test_get_day_with_most_views_no_response(mock_get_articles_request):
    """
    Tests that when calling get_day_with_most_views() with article title, year, and month
    and the Wikipedia API returns with no data, a null date is returned.
    """
    article_title = "test1"
    year = 2020
    month = 3
    start = f'{year}{month:02d}01'
    end = f'{year}{month:02d}31'

    date = WikipediaAPIWrapper().get_day_with_most_views(article_title, year, month)

    expected_url = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"
    mock_get_articles_request.assert_called_with(expected_url)
    assert date is None
