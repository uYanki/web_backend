# 内容: 路由参数, 重定向, 模板

from flask import Flask, url_for, request, redirect, render_template
# template_folder: 设置模板的根路径 (用于 render_template), 默认为 templates
app = Flask(__name__, template_folder='templates')


@app.route('/login', methods=['GET', 'POST'])
def login():  # 登录界面
    if request.method == 'POST':
        print('post-data', request.form)
        return '登录成功'
    elif request.method == 'GET':
        print('get')
        # 模板传参1
        context1 = {"tip": "please login"}
        # 模板传参2
        context2 = {"links": {
            "https://www.bing.com",
            "https://www.360.com",
        }}
        # 渲染模板(html), 以下两种模板参数在模板内的访问方式是不同的
        return render_template('login.html', **context1, sites=context2)


@app.route('/user', methods=['GET'])
def user():
    user_id = request.args.get("uid")
    # http://127.0.0.1:5000/user?uid=1
    if user_id:
        return '个人中心'
    # 没有 user_id 就跳转至登录界面
    return redirect(url_for('login'), code=302)
    # code: 301:永久性重定向 302:暂时性重定向


if __name__ == "__main__":
    app.run(debug=True)
