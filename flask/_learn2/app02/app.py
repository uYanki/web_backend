import os

from flask import Flask, flash, render_template, g, current_app

app = Flask(__name__)
app.secret_key = "dev"


@app.route('/')
def index():
    # https://dormousehole.readthedocs.io/en/latest/templating.html
    # 默认情况下, Jinja2 可使用 flask 中的
    # - 全局变量: config, request, session, g
    # - 函数: url_for(), get_flashed_messages()

    g.name = "uYanki"  # 用于传参

    flash('error')  # 在模板渲染时使用 (存在session['_flashes']里)

    style = '<span style="color:red;">hello</span>'

    return render_template('index.html', style=style)


#########################################

# 自定义 过滤器 (2种方法):

@app.template_filter('dblstr')
def dlbstr_filter(s):
    return s * 2

# def dblstr_filter(s):
#     return s * 2
# app.jinja_env.filters['dblstr2'] = dblstr_filter

#########################################

# 自定义 环境处理器 / 上下文处理器


@app.context_processor
def inject_user():
    return dict(user={'name': 'uYanki', 'age': 20})


@app.context_processor
def utility_processor():
    def format_price(amount, currency="€"):
        return f"{amount:.2f}{currency}"
    return dict(format_price=format_price)


if __name__ == '__main__':
    app.run(debug=True)
