import os
from werkzeug.utils import secure_filename
from ..db import db
from ..models.news_model import News
from bson import ObjectId
from flask import current_app

UPLOAD_FOLDER = "app/static/uploads/news"

def get_all_news():
    raw_news = db.news.find()

    news = []
    for item in raw_news:
        news_obj = News.from_dict(item)

        news_data = news_obj.to_dict()
        news_data['id'] = str(news_obj.id)

        news.append(news_data)

    return news

def add_news(title, content, image_file=None):
    image_path = None

    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(save_path)

        image_path = f"/static/uploads/news/{filename}"

    news_obj = News(title=title, content=content, image=image_path)
    db.news.insert_one(news_obj.to_dict())


def delete_news(news_id):
    news = db.news.find_one({"_id": ObjectId(news_id)})
    if not news:
        return

    image_path = news.get("image")

    if image_path:
        relative_path = image_path.lstrip("/")
        full_path = os.path.join(current_app.root_path, relative_path)

        if os.path.exists(full_path):
            os.remove(full_path)
            print("Deleted file:", full_path)
        else:
            print("File not found:", full_path)

    db.news.delete_one({"_id": ObjectId(news_id)})