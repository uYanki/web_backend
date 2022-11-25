import os

from flask import Flask, make_response, url_for, redirect, request, render_template, session
from markupsafe import escape

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#####################################################


@app.route('/')  # 将函数绑定至URL
def index():
    # eg: http://127.0.0.1:5000/
    # url_for: 反向解析,通过函数名获取URL
    # redirect: 重定向页面
    return redirect(url_for("hello", name='world'))


@app.route('/hello/')  # 无参
@app.route('/hello/<string:name>')  # 有参
# 路由转换器(高级的还可以自定义)
# string  不包含斜杠的字符串(默认)
# int     正整数
# float   正浮点数
# path    可包含斜杠的字符串
# uuid    uuid字符串
def hello(name=None):
    # eg: http://127.0.0.1:5000/hello/uYanki
    # escape: html 字符转义
    if name is None:
        name = "uYanki"
    # return f'<script>alert("hello {name}")</script>'
    return escape(f'<script>alert("hello {name}")</script>')

#####################################################


# 重定向行为: URL后加上'/',访问时不带'/'就会自动重定向到带'/'的, 两种差别不大,统一风格即可

@app.route('/docs')
def docs():
    # eg: http://127.0.0.1:5000/docs  访问成功
    # eg: http://127.0.0.1:5000/docs/ 访问报错
    return 'docs'


@app.route('/books/')
def books():
    # eg: http://127.0.0.1:5000/books  访问成功
    # eg: http://127.0.0.1:5000/books/ 访问成功
    return 'books'

#####################################################

# 模板默认路径为 templates, 可在 Flask.__init__() 中查看


@app.errorhandler(404)  # 自定义错误处理
def notfound(error):
    return render_template('404.html'), 404
    # 404 代表页面不存在, 默认返回的是 200


@app.route('/user/center/')
def user_center():
    # eg: http://127.0.0.1:5000/user/center/

    # 关闭浏览器后 cookies 没了, 但 session 还存在, 因为 session 存在服务器上

    usr = request.cookies.get('username')
    print(request.headers.get('hello'))  # 输出None,自定的响应头的数据无法到达

    if usr == '' and 'username' in session:
        # 移除: session.pop('username', None)
        # 在设置 session 字段是, session 会自动记录其他信息, 用于识别
        usr = session.get('username')
        return f'session_username:{usr}'

    return f'username:{usr}'


@app.route('/login/', methods=['GET', 'POST'])
# 使用 methods 指定允许的 HTTP 方法,默认只响应 GET请求
def login():
    # eg: http://127.0.0.1:5000/login/
    # eg: http://127.0.0.1:5000/login/?name=uYanki

    error = None
    if request.method == 'POST':
        # post 请求需从 form 表单获取数据
        usr = request.form.get('usr')
        pwd = request.form.get('pwd')
        if usr != '' and pwd == '1234':
            # 自定义响应体
            resp = make_response(redirect(url_for("user_center")))
            resp.headers['hello'] = 'hello wrold'  # 往响应头中添加字段
            resp.set_cookie('username', usr)  # 设置 cookies ( F12 - 应用 查看保存的 cookies )
            # 使用 session 是需配置密钥(app.secret_key)
            session['username'] = usr  # 设置 session (用不同浏览器登录不会覆盖字段,并且浏览器关闭后,原session失效)
            return resp
        error = 'Invalid username/password'

    # 从 url (?key=value) 获取参数
    name = request.args.get('name')

    # 与django一样,都是使用JinJa2渲染模板
    return render_template('login.html', name=name, error=error)


@app.route('/upload', methods=['GET', 'POST'])  # 文件上传例子
# 详细: https://dormousehole.readthedocs.io/en/latest/patterns/fileuploads.html
def upload_file():
    # http://127.0.0.1:5000/upload
    if request.method == 'POST':
        file = request.files['file']
        path = f'./upload/{file.filename}'
        file.save(path)  # 需提前创建目录
        return 'success' if os.path.exists(path) else 'fail'
    return render_template('upload.html')

#####################################################


if __name__ == '__main__':
    app.run(debug=True)  # 本机调试
    # app.run(host='0.0.0.0', port=80) # 局域网范围内可访问
