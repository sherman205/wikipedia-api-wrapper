"""
Flask routes for Wikipedia API wrapper
"""

from flask import Flask, jsonify, request, render_template
from wikipedia.wikipedia_api import WikipediaAPIWrapper
from exception import CustomException

app = Flask(__name__)
wrapper = WikipediaAPIWrapper()


@app.route('/')
def wikipedia_api_home():
    """Index route on app load."""
    return "Welcome to the Wikipedia API Flask App!"


@app.route('/most_viewed_articles')
def get_most_viewed_articles():
    """Endpoint that returns a list of articles with the most views."""
    year = int(request.args.get('year', 2023))
    month = int(request.args.get('month', 1))

    day = request.args.get('day')
    start_day = request.args.get('start_day')
    end_day = request.args.get('end_day')

    day = int(day) if day else None
    start_day = int(start_day) if start_day else None
    end_day = int(end_day) if end_day else None

    try:
        articles = wrapper.get_most_viewed_articles(year, month, day, start_day, end_day)
        return jsonify(articles)
    except CustomException as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/article_view_count/<article_title>')
def get_article_view_count(article_title):
    """Endpoint that returns the view count for a specific article."""
    year = int(request.args.get('year', 2023))
    month = int(request.args.get('month', 1))

    start_day = request.args.get('start_day')
    end_day = request.args.get('end_day')

    start_day = int(start_day) if start_day else None
    end_day = int(end_day) if end_day else None

    try:
        view_count = wrapper.get_article_view_count(article_title, year, month, start_day, end_day)
        return jsonify({'article': article_title, 'view_count': view_count})
    except CustomException as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.route('/most_views_day/<article_title>')
def get_most_views_day(article_title):
    """Endpoint that returns the day with the most views for an article."""
    year = int(request.args.get('year', 2023))
    month = int(request.args.get('month', 1))

    try:
        most_views_day = wrapper.get_day_with_most_views(article_title, year, month)
        return jsonify({'article': article_title, 'most_views_day': most_views_day})
    except CustomException as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
