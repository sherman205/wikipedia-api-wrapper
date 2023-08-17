import requests
import calendar
from flask import request


class WikipediaAPIWrapper:
    def __init__(self):
        self.base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews"

    def get_most_viewed_articles(self, year, month, day):
        url_suffix = f"top/en.wikipedia/all-access/{year}/{month:02d}/{day:02d}"
        articles_data = self._get_articles_request(url_suffix)
        return articles_data

    def get_article_view_count(self, article_title, year, month, day):
        start = f"{year}{month:02d}{day:02d}"
        end = f"{year}{month:02d}{day:02d}"
        url_suffix = f"per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start}/{end}"
        articles_data = self._get_articles_request(url_suffix)

        view_count = 0
        for article_data in articles_data:
            if article_data['article'] == article_title:
                view_count += article_data['views']
        return view_count

    def get_day_with_most_views(self, article_title, year, month):
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

        return max_views_day

    def _get_articles_request(self, url):
        url = f"{self.base_url}/{url}"
        headers = {'User-Agent': request.headers.get('User-Agent')}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            articles_data = data.get('items', [])
            return articles_data
        else:
            print("Failed to retrieve data from the API.")
            return []
