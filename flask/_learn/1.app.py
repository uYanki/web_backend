# 内容: 基本配置, json, list

from flask import Flask, jsonify

# 初始化Flask实例
print(__name__)
app = Flask(__name__)

'''项目基本配置'''
# method ① 直接配置
# app.config['JSON_AS_ASCII'] = False
# method ② 文件导入
import settings
app.config.from_object(settings)


@app.route('/')  # 根路径
@app.route('/index')
# 使用装饰器将URL映射到函数上
def index():
    return 'hello world'


@app.route('/json')
def json():
    # 当返回值是返回字典时, flask 会将其自动转化为Json.
    # 如涉及中文, 需配置 app.config['JSON_AS_ASCII'] = False, 
    # 将响应头设置为 "application/json;charset=utf-8", 否则响应报文中的中文会显示乱码.
    return {'data_en': 'hello', 'data_zh': '你好'}


@app.route('/list')
def list():
    # 需使用 jsonify 将列表格式化后才能返回
    return jsonify([{"min": 1, "max": 1},
                    {"min": 2, "max": 2},
                    {"min": 3, "max": 3}])


if __name__ == "__main__":
    app.run(debug=True)  # 调试模式: http://127.0.0.1:5000/ (端口默认5000)
    # app.run(host='0.0.0.0', port=80) # 启用局域网/外网访问: host='0.0.0.0'
