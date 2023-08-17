from flask import Flask, jsonify, request
from wikipedia.wikipedia_api import WikipediaAPIWrapper

app = Flask(__name__)
wrapper = WikipediaAPIWrapper()


@app.route('/')
def wikipedia_api_home():
    return "Welcome to the Wikipedia API Flask App!"


@app.route('/most_viewed_articles')
def get_most_viewed_articles():
    year = int(request.args.get('year', 2023))
    month = int(request.args.get('month', 1))

    day = request.args.get('day')
    start_day = request.args.get('start_day')
    end_day = request.args.get('end_day')

    day = int(day) if day else None
    start_day = int(start_day) if start_day else None
    end_day = int(end_day) if end_day else None

    articles = wrapper.get_most_viewed_articles(year, month, day, start_day, end_day)
    return jsonify(articles)


@app.route('/article_view_count/<article_title>')
def get_article_view_count(article_title):
    year = int(request.args.get('year', 2023))
    month = int(request.args.get('month', 1))

    start_day = request.args.get('start_day')
    end_day = request.args.get('end_day')

    start_day = int(start_day) if start_day else None
    end_day = int(end_day) if end_day else None

    view_count = wrapper.get_article_view_count(article_title, year, month, start_day, end_day)
    return jsonify({'article': article_title, 'view_count': view_count})


@app.route('/most_views_day/<article_title>')
def get_most_views_day(article_title):
    most_views_day = wrapper.get_day_with_most_views(article_title, 2022, 11)
    return jsonify({'article': article_title, 'most_views_day': most_views_day})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
