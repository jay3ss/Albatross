from flask import Blueprint


bp = Blueprint("articles", __name__)


from app.articles import routes
