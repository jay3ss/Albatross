from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.articles import bp
from app.models import Article


@bp.route("/")
@login_required
def articles():
    articles = Article.query.filter_by(user=current_user).all()
    return render_template("articles/articles.html", articles=articles)


@bp.route("/<slug>")
@login_required
def article(slug):
    article = Article.query.filter_by(slug=slug).first()
    return render_template("articles/article.html", article=article)
