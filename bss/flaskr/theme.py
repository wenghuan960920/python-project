# 管理员主题的增删改查
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_requireduser
from .model import User as u, Post as p, Theme as t, Reply as r
from .db import db


bp = Blueprint('theme', __name__)


@bp.route('/indextheme')
def indextheme():

    themes = db.session.query(t.theme_id, t.author_id, t.theme_created, t.theme_text).order_by(t.theme_created.desc()).all()

 

    return render_template('blog/admin/indextheme.html', themes=themes)


def get_theme(theme_id):

    theme = db.session.query(t.theme_id, t.theme_created, t.theme_text).order_by(t.theme_created.desc()).first()
   
    if theme is None:
        abort(404, "Post id {0} doesn't exist.".format(theme_id))

    return theme


@bp.route('/createtheme', methods=('GET', 'POST'))
@login_requireduser
def createtheme():
    if request.method == 'POST':
        theme_text = request.form['theme_text']
        error = None

        if not theme_text:
            error = 'theme is required.'

        if error is not None:
            flash(error)

        else:
            theme = t(g.user.user_id, theme_text)
            db.session.add(theme)
            
            db.session.commit()
            return redirect(url_for('theme.indextheme'))

    return render_template('blog/admin/createtheme.html')


@bp.route('/<int:theme_id>/updatetheme', methods=('GET', 'POST'))
@login_requireduser
def updatetheme(theme_id):
    theme = get_theme(theme_id)

    if request.method == 'POST':
        theme_text = request.form['theme_text']
        error = None

        if not theme_text:
            error = 'theme_text is required.'

        if error is not None:
            flash(error)
        else:
            p.query.filter_by(theme_id=theme_id).update({
                'theme_text': theme_text,
            })
            db.session.commit()
            return redirect(url_for('theme.indextheme'))

    return render_template('blog/admin/updatetheme.html', theme=theme)


@bp.route('/<int:theme_id>/delete', methods=('POST',))
@login_requireduser
def deletetheme(theme_id):
    get_theme(theme_id)
    db.session.query(t).filter(t.theme_id==theme_id)
    db.session.commit()
    return redirect(url_for('theme.indextheme'))