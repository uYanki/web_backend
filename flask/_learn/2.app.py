# 内容: 路由参数, 反向解析

from flask import Flask, jsonify, url_for


print(__name__)
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


books = [{'id': 1, 'name': '三国演义'},
         {'id': 2, 'name': '水浒传'},
         {'id': 3, 'name': '红楼梦'},
         {'id': 4, 'name': '西游记'}]


@app.route('/search/<int:book_id>')
@app.route('/search/<string:book_name>')
def search(book_id=0, book_name=""):  # 带参GET请求
    # flask 会自动识别参数类型
    print(book_id, book_name)

    for book in books:
        if book['id'] == book_id or book['name'] == book_name:
            return book  # 返回字典

    if book_id != 0:
        return f'can\'t find book which id is {book_id}'
    return f'can\'t find book which name is {book_name}'


@app.route('/list')
def list():
    for book in books:
        # url 的反向解析, 通过视图函数获取访问路径
        book['url'] = url_for("search", book_id=book['id'])
    return jsonify(books)


if __name__ == "__main__":
    app.run(debug=True)
