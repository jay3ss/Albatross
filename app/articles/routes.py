from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.articles import bp, forms
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


@bp.route("/new", methods=["get", "post"])
def create_article():
    form = forms.CreateArticleForm()
    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            content=form.content.data,
            # image_url=form.image_url,
            summary=form.summary.data
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("articles.article", slug=article.slug))
    return render_template("articles/new.html", form=form)
