"""
Information about wikipedia articles using Wikipedia API
"""

import requests
import calendar
from flask import request, current_app
from datetime import timedelta, datetime


class WikipediaAPIWrapper:
    def __init__(self):
        self.base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews"

    def get_most_viewed_articles(self, year, month, day=None, start_day=None, end_day=None):
        """Returns a list of the top 1000 most viewed articles for a week or a month."""
        # API querying based on specific day
        if day:
            url_suffix = f"top/en.wikipedia/all-access/{year}/{month:02d}/{day:02d}"
        # API querying based on specific month
        else:
            url_suffix = f"top/en.wikipedia/all-access/{year}/{month:02d}/all-days"

        # API querying based on date range
        articles_data = []
        if start_day and end_day and not day:
            start_date = datetime(year, month, start_day)
            end_date = datetime(year, month, end_day)
            delta = timedelta(days=1)

            # start and end date inclusive
            while start_date <= end_date:
                url_suffix = f"top/en.wikipedia/all-access/{start_date.year}/" \
                             f"{start_date.month:02d}/{start_date.day:02d}"

                articles_response = self._get_articles_request(url_suffix)
                articles_response = articles_response[0]['articles'] if articles_response else []

                existing_articles = {a['article']: a for a in articles_data}
                for new_article, article_name in ((new_article, new_article['article'])
                                                  for new_article in articles_response):
                    # If article already exists in list, add to the total view count
                    if article_name in existing_articles:
                        existing_article = existing_articles[article_name]
                        updated_views = existing_article["views"] + new_article["views"]

                        existing_article['views'] = updated_views
                    # Article isn't recorded yet, create a new entry in the list
                    else:
                        existing_articles[article_name] = new_article

                # Only store up-to-date articles, no duplicates
                articles_data.clear()
                articles_data.extend(existing_articles.values())

                start_date += delta
        else:
            articles_data = self._get_articles_request(url_suffix)
            articles_data = articles_data[0]['articles'] if articles_data else []

        # top 1000 most viewed articles, consistent with Wikipedia's API for list of most viewed articles
        return articles_data[:1000]

    def get_article_view_count(self, article_title, year, month, start_day=None, end_day=None):
        """Returns the view count for a specific article for a week or a month."""
        if start_day and end_day:
            start = f"{year}{month:02d}{start_day:02d}"
            end = f"{year}{month:02d}{end_day:02d}"
        else:
            days_in_month = calendar.monthrange(year, month)[1]
            start = f"{year}{month:02d}01"
            end = f"{year}{month:02d}{days_in_month}"

        url_suffix = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"

        articles_data = self._get_articles_request(url_suffix)

        view_count = 0
        for article_data in articles_data:
            if article_data['article'] == article_title:
                view_count += article_data['views']
        return view_count

    def get_day_with_most_views(self, article_title, year, month):
        """Returns the date when an article got the most page views."""
        days_in_month = calendar.monthrange(year, month)[1]
        start = f"{year}{month:02d}01"
        end = f"{year}{month:02d}{days_in_month}"
        url_suffix = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"
        articles_data = self._get_articles_request(url_suffix)
        max_views = 0
        max_views_day = None

        for article_data in articles_data:
            if article_data['article'] == article_title:
                views = article_data['views']
                timestamp = article_data['timestamp']
                if article_data['views'] > max_views:
                    max_views = views
                    max_views_day = timestamp

        date = datetime.strptime(max_views_day, '%Y%m%d%H').strftime('%m/%d/%Y') if max_views_day else None
        return date

    def _get_articles_request(self, url):
        """Base request function for the Wikipedia API."""
        url = f"{self.base_url}/{url}"
        headers = {'User-Agent': request.headers.get('User-Agent')}

        try:
            response = requests.get(url, headers=headers)
            # raise exception if not 200 status
            response.raise_for_status()

            data = response.json()
            articles_data = data.get('items', [])
        except requests.HTTPError as e:
            current_app.logger.info(f"Failed to retrieve data from the API: {e}")
            articles_data = []

        return articles_data
