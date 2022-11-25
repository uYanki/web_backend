import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    # g.user 会传给 base.html 用于判断用户是否已登录
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/register/', methods=['GET', 'POST'])
def register():  # 注册
    if request.method == 'POST':

        error = None
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required.'

        db = get_db()

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                    # 为了安全起见, 不以明文存入数据库, 而以哈希值存入
                )
                db.commit()
            except db.IntegrityError:  # 用户已存在,报错
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))  # 跳转到登录页面

        flash(error)  # 在模板文件中使用 get_flashed_messages() 获取错误

    return render_template('auth/register.html')


@bp.route('/login/', methods=('GET', 'POST'))
def login():  # 登入
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()  # fetchone: 取单个, fetchall: 取全部.

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']  # 记录 uid
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout/')
def logout():  # 登出
    session.clear()
    return redirect(url_for('index'))


def login_required(view):  # 权限校验
    # 装饰器原理:闭包函数
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
