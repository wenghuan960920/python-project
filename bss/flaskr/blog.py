# 博客的增删改查
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app
from werkzeug.exceptions import abort
from flaskr.auth import login_requireduser
from .model import User as u, Post as p, Theme as t, Reply as r
from .db import db


bp = Blueprint('blog', __name__)


@bp.route('/')
def indexblog():

    blogs = db.session.query(p.post_id,p.post_title, p.post_body, p.post_created, p.author_id, t.theme_text, u.username).filter(u.user_id == p.author_id, t.theme_id == p.theme_id).order_by(p.post_created.desc())

   
    return render_template('blog/user/indexblog.html', posts=blogs)


@bp.route('/<int:post_id>/indexone', methods=('GET', 'POST'))
def indexone(post_id):
    if request.method == 'GET':
        blog = db.session.query(p.post_id, p.post_title, p.post_body, p.post_created, p.author_id, t.theme_text, u.username).filter(p.author_id ==u.user_id, t.theme_id==p.theme_id, post_id == post_id).first()
        replys = db.session.query(r.reply_id, u.username, r.post_id, r.reply_created, r.reply_text).filter(
               r.post_id==post_id).all()
        db.session.commit()

        if replys is None:
            render_template('blog/context.html', post=blog, replys=replys)

    if request.method == 'POST':

        reply_text = request.form['reply_text']
        reply1 = r(g.user.user_id, post_id, reply_text)
        print(f'reply1:{reply1}')
        db.session.add(reply1)
        db.session.commit()
        return redirect(url_for('blog.indexone', post_id=post_id))

    return render_template('blog/context.html', post=blog, replys=replys)


def get_blog(post_id, check_author=True):

    post = db.session.query(p.post_id, p.post_title, p.post_body, p.post_created, p.author_id, t.theme_text, u.username).filter(t.theme_id  == p.theme_id, p.author_id == u.user_id, p.post_id==post_id).first()
   

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(post_id))

    if check_author and post.author_id !=  g.user.user_id:
        abort(403)

    return post


@bp.route('/createblog', methods=('GET', 'POST'))
@login_requireduser
def createblog():
    themes = db.session.query(t).all()

    db.session.commit()
   
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']
        theme_id = request.form['theme_id']
        error = None

        if not post_title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            post1 = p( g.user.user_id, theme_id, post_title, post_body)
            db.session.add(post1)
            db.session.commit()
        return redirect(url_for('blog.indexblog'))
    print('themes is [{}]'.format(themes))
    print(f'{isinstance(themes,list)}isinstance(list,themes),{type(themes)}')

    return render_template('blog/user/createblog.html', themes=themes)


@bp.route('/<int:post_id>/updateblog', methods=('GET', 'POST'))
@login_requireduser
def updateblog(post_id):
    post = get_blog(post_id)
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']
        error = None

        if not post_title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            p.query.filter_by(post_id=post_id).update({
                'post_title': post_title,
                'post_body':post_body,
            })
            db.session.commit()
        return redirect(url_for('blog.indexblog'))

    return render_template('blog/user/updateblog.html', post=post)


@bp.route('/<int:post_id>/deleteblog',methods=('POST',))
@login_requireduser
def deleteblog(post_id):
    get_blog(post_id)
    post = p.query.filter_by(post_id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.indexblog'))
