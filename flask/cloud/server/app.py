import os

from flask import Flask, jsonify, render_template, send_from_directory, url_for, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

import lib_oper_records as oper_db

app = Flask(__name__)
CORS(app, resources=r'/*')  # 开启跨域请求

upload_path = './data'

########### 信息查看 ###########


@app.route('/', methods=['GET'], strict_slashes=False)
@app.route('/disk', methods=['GET'], strict_slashes=False)
@app.route('/disk/<path:dirpath>', methods=['GET'], strict_slashes=False)
def enum_disk(dirpath=''):  # localhost:5000/disk
    return render_template("disk.html", root=url_for('enum_disk', path=''), dir=url_for('oper_disk', path=dirpath))


# 访问path路径任意, 在上传文件的文件后, 会自动生成路径
@app.route('/api/oper_disk/', methods=['GET', 'POST'], strict_slashes=False)
@app.route('/api/oper_disk/<path:path>', methods=['GET', 'POST'], strict_slashes=False)
def oper_disk(path=''):
    if request.method == "POST":  # upload file
        # path == '' -> data 根目录
        f = request.files['file']
        try:
            os.makedirs(os.path.join(upload_path, path))  # 创建目录
        except Exception:  # 目录已创建就跳过创建
            pass
        filename = os.path.join(upload_path, path, secure_filename(f.filename))
        f.save(filename)
        return 'sucess'
    # list disk
    url_dirs = []
    url_files = []
    url_path = url_for('oper_disk', path=path)  # dirpath
    for root, dirs, files in os.walk(os.path.join(upload_path, path)):
        print(dirs, files, root)
        for dir in dirs:
            url_dirs.append({"name": dir,
                             "path": path + '/' + dir,
                             "url": url_for('enum_disk', dirpath=path + '/' + dir)})  # 用 os.path.join 会导致 json 里错乱
        for file in files:
            url_files.append({"name": file,
                              "path": path + '/' + file,
                              "url": url_for('fench_file', filepath=path + '/' + file)})
        break
    return jsonify(path=url_path, dirs=url_dirs, files=url_files)


@ app.route('/api/get_file/<path:filepath>')
def fench_file(filepath):
    print('/api/get_file/' + filepath)
    return send_from_directory(upload_path, filepath)


########### 操作记录(未启用) ###########


@ app.route('/api/list_records', methods=['GET'])
def operation_records():  # 操作记录
    records = oper_db.db_list(10)
    return records


########### 启动服务器 ###########

oper_db.db_init()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
