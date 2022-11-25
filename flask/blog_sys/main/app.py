
import os

from flask import Flask


app = Flask(__name__, instance_relative_config=True)
# instance_relative_config: 将数据库等文件与版本控制分离

if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)  # 实例目录创建

import config
app.config.from_object(config)

# 数据库存放路径: /instance/db.sqlite
app.config['DATABASE'] = os.path.join(app.instance_path, 'db.sqlite')

import db
db.init_app(app)

import auth
app.register_blueprint(auth.bp)

import blog
app.register_blueprint(blog.bp)
# 类似django的路由绑定,endpoint值为视图函数
app.add_url_rule('/', endpoint='index')


app.run(debug=True)
# app.run(host='0.0.0.0', port=80)
