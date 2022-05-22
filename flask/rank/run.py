# https://www.w3cschool.cn/flask/

import random
from datetime import datetime

import sqlite3 as sql
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)

# 开启跨域请求
CORS(app, resources=r'/*')

db_name = 'database.db'  # 数据库名
db_table_name = 'rank'  # 表名


def db_init():
    # 创建数据库和数据表
    db = sql.connect(db_name)
    db.execute(f"CREATE TABLE IF NOT EXISTS {db_table_name} (name TEXT, score INT, time TEXT DEFAULT (datetime('now','localtime')))")  # 创建表

    # 生成随机数据
    def random_data():
        cur = db.cursor()
        charset = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        for i in range(50):
            name = ""
            for j in range(6):  # 随机名
                name += charset[random.randint(0, len(charset) - 1)]
            cur.execute(f"INSERT INTO {db_table_name} (name,score,time) VALUES (?,?,datetime('now'))",
                        (name, random.randint(0, 100)))  # 添加数据
        db.commit()
    # random_data()

    # 关闭数据库
    db.close()


db_init()


@ app.route('/')
@ app.route('/index')
def index():  # 排行榜
    return render_template('rank.html')


@ app.route('/add')
def view_add():  # 数据添加
    return render_template('add.html')


@ app.route('/api/top', methods=['GET'])
def api_top():
    db = sql.connect(db_name)  # 连接数据库
    db.row_factory = sql.Row
    cur = db.cursor()
    cur.execute(f"select * from {db_table_name} order by score desc")  # 降序排序 (不支持中文模糊搜索)
    row = cur.fetchall()[0]  # 取前9条数据
    rank = {"name": row["name"], "score": row["score"], "datetime": row["time"]}
    return jsonify(rank)


# request.form:用于接收表单参数
# request.args:用于接收GET参数
# request.json:用于接收JSON参数
# request.values:获取所有参数(表单参数+GET参数)
# request.file:用于接收文件
@ app.route('/api/rank/', methods=['POST', 'GET'])
def api_rank():
    if request.method == 'POST':  # add record
        # [headers] Content-Type:
        # form格式:application/x-www-form-urlencoded
        # json格式:application/json
        data = request.form.to_dict()
        if data == {}:
            data = request.json
        print(data, data['name'], data['score'])
        try:
            with sql.connect(db_name) as db:
                cur = db.cursor()
                cur.execute(f"INSERT INTO {db_table_name} (name,score) VALUES (?,?)",
                            (data['name'], int(data['score'])))   # 添加数据至数据库
                db.commit()
            return jsonify("ok")
        except Exception:
            print("errrrr")
            return jsonify("err")

    elif request.method == 'GET':  # list records

        db = sql.connect(db_name)  # 连接数据库
        db.row_factory = sql.Row
        cur = db.cursor()

        keyword = request.args.get('keyword')  # 取出参数
        cur.execute(f"select * from {db_table_name} where name like \"%{keyword}%\" order by score desc")  # 降序排序 (不支持中文模糊搜索)
        rows = cur.fetchall()[:99]  # 取前9条数据

        rank = []
        for row in rows:  # 生成rank
            rank.append({"name": row["name"], "score": row["score"], "datetime": row["time"]})
        return jsonify(rank)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
