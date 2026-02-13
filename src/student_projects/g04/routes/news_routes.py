from flask import Blueprint, render_template, request, redirect, url_for
from ..services.news_service import get_all_news, add_news, delete_news

news_bp = Blueprint('news', __name__)

@news_bp.route('/news', methods=['GET'])
def list_news():
    news = get_all_news()
    return render_template('news/index.html', news=news)


@news_bp.route('/news/add', methods=['GET', 'POST'])
def add_news_route():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        if title and content:
            add_news(title, content, image)
            return redirect(url_for('news.list_news'))

    return render_template('news/add.html')


@news_bp.route('/news/delete/<news_id>', methods=['POST'])
def delete_news_route(news_id):
    delete_news(news_id)
    return redirect(url_for('news.list_news'))