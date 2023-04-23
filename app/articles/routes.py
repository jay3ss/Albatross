from flask import (current_app, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required

from app import db
from app.articles import bp, forms
from app.models import Article


@bp.route("/")
@login_required
def articles():
    per_page = current_app.config["ARTICLES_PER_PAGE"]
    page = request.args.get("page", 1, type=int)
    pagination = (
    Article
        .query
        .filter_by(user=current_user)
        .paginate(page=page, per_page=per_page)
    )
    articles = pagination.items
    return render_template(
        "articles/articles.html",
        articles=articles,
        Article=Article,
        pagination=pagination
    )


@bp.route("/<slug>")
@login_required
def article(slug):
    article = db.first_or_404(db.select(Article).filter_by(slug=slug))
    return render_template("articles/article.html", article=article)


@bp.route("/new", methods=["get", "post"])
@login_required
def create_article():
    form = forms.CreateArticleForm()
    if form.validate_on_submit():
        article = Article()
        form.populate_obj(article)
        article.user = current_user
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("articles.article", slug=article.slug))
    return render_template("articles/new.html", form=form)


@bp.route("/<slug>/edit", methods=["get", "post"])
@login_required
def edit_article(slug):
    article = db.first_or_404(db.select(Article).filter_by(slug=slug))
    form = forms.EditArticleForm()
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.commit()
        return redirect(url_for("articles.article", slug=slug))
    form = forms.EditArticleForm(obj=article)
    return render_template("articles/edit.html", form=form, article=article)


@bp.route("/<slug>/delete", methods=["post"])
@login_required
def delete_article(slug):
    article = db.first_or_404(db.select(Article).filter_by(slug=slug))
    if article.user_id == current_user.id:
        db.session.delete(article)
        db.session.commit()
        flash("Article has been deleted.")
        return redirect(url_for("articles.articles"))
    flash("You can't delete articles that don't belong to you.")
    return redirect(url_for("articles.articles"))
