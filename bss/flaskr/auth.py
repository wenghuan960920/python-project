# 用户的增退登
import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash
# from .model import u, p, t, r
from .model import User as u
from .db import db


#会在这个下面找蓝图，生成组合蓝图，注意此处已经添加了unlogin所以可能不可以。
bp = Blueprint('auth', __name__, url_prefix='/auth')


#######这里不能很好的理解
def login_requireduser(view):
    @functools.wraps(view)                            #包装饰器，在装饰函数的时候，不改变函数本身的属性。
    def wrapped_view(**kwargs):                       #表传入
        if g.user is None:
            return redirect(url_for('auth.loginuser'))#如果不存在跳转到登录函数，登录函数生成htnl界面

        return view(**kwargs)                         #字典显示

    return wrapped_view


#每次请求前执行，确保登陆并且拿到当前登录用户信息。
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
        print('g.user加载到里面了')
    else:                               #如果user_id存在，则去数据库查找
        g.user = u.query.filter_by(user_id=user_id).first()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['user_password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif u.query.filter_by(username=username).first() is not None:
            error = 'User {0} is already registered.'.format(username)

        if error is None:     #插入语句
            user1 = u(username, generate_password_hash(password),0)
            db.session.add(user1)
        db.session.commit()   #这里是对数据库的刷新。

        return redirect(url_for('auth.logout'))
        flash(error)
    return render_template('auth/register.html')


@login_requireduser
@bp.route('/setuser', methods=('GET', 'POST'))
def setuser():

    if request.method == 'POST':
        password = request.form['user_password']
        error = None

        if not password:
            error = 'Password is required.'

        if error is None:
            u.query.filter_by(user_id=g.user.user_id).filter_by(user_sign=0).update({
                'user_password':generate_password_hash(password)
            })

            db.session.commit()                   #这里是对数据库的刷新
            return redirect(url_for('auth.logout'))

        flash(error)
    return render_template('auth/setperson.html')


# 当login页面触发时，根据login页面的按钮触发的不同，跳转到不同的URL
@bp.route('/loginuser', methods=('GET', 'POST'))
def loginuser():
    if  request.method == 'POST':
        username = request.form['username']
        user_password = request.form['user_password']
        erroruser = None
        #这里是对数据库的查询
        user = u.query.filter(u.username == username).first()
        print(f'user.username:{user.username}')
        # current_app.logger.info('%s logged in successfully', user.userpassword)
        if user is None:
            erroruser = 'Incorrect username.'
        # (username, generate_password_hash(password), 0)=============
        # if admin is None:
        #     print('进入了插入数据')
        #     db.execute(
        #         'INSERT INTO admin(adminame, admin_password) VALUES (?, ?) ',
        #         ('111', 111)
        #     )
        elif user.user_sign == 1:
            u.query.filter_by(username=username).update({
                'username':username,
                'user_password': generate_password_hash(user_password)
            })

        elif not check_password_hash(user.user_password, user_password) == True:
        # elif not check_password_hash(user['user_password'], user_password):
            erroruser = 'Incorrect password.'

        print(f'erroruser:{erroruser}')
        if erroruser is None:
            session.clear()
            print(f'user.user_id:{user.user_id}')
            session['user_id'] = user.user_id

            if user.user_sign == 0:
                # 索引的位置是blog的索引显示，blog在去查询数据库并调用。
                return redirect(url_for('blog.indexblog'))
            elif user.user_sign == 1:
                return redirect(url_for('theme.indextheme'))
        flash(erroruser)
    return render_template('auth/userlogin.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('indexblog'))