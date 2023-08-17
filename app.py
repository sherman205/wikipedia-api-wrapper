from flask import Flask, jsonify
from wikipedia.wikipedia_api import WikipediaAPIWrapper

app = Flask(__name__)
wrapper = WikipediaAPIWrapper()


@app.route('/')
def hello_world():
    return "Welcome to the Wikipedia API Flask App!"


@app.route('/most_viewed_articles')
def get_most_viewed_articles():
    articles = wrapper.get_most_viewed_articles(2022, 11, 10)
    return jsonify(articles)


@app.route('/article_view_count/<article_title>')
def get_article_view_count(article_title):
    view_count = wrapper.get_article_view_count(article_title, 2022, 11, 10)
    return jsonify({'article': article_title, 'view_count': view_count})


@app.route('/most_views_day/<article_title>')
def get_most_views_day(article_title):
    most_views_day = wrapper.get_day_with_most_views(article_title, 2022, 11)
    return jsonify({'article': article_title, 'most_views_day': most_views_day})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
