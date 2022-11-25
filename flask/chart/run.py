# https://www.w3cschool.cn/flask/

import math
from random import randint
from datetime import datetime, timedelta

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)

# 开启跨域请求
CORS(app, resources=r'/*')

# pyinstaller -F run.py -w
import numpy as np
from scipy import fftpack

# 傅里叶变换结果
_freq = []
_freq_sig = []
_len = 0

_is_change = False

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route("/api/mic", methods=['get', 'post'])
def mic():
    global _freq, _freq_sig, _len, _is_change

    if request.method == "POST":

        # 接收128点的数据, 并进行傅里叶变换

        # 上传数据
        try:
            # print(request.data)

            data = request.json['data']  # 获取esps上传的数据
            '''
            "header": Content-Type:application/json
            "body":
                {
                    "data": {
                        "mic": "1,2,4",
                        "len": "3",
                        "freq": "18000"
                    }
                }
            '''

            mic = data["mic"].split(",")  # 原始数据
            print(mic)
            cnt = int(data["len"])  # 数据点数
            hz = int(data["freq"])   # 采样频率
            # hz = 128

            # print(mic, cnt, hz)

            # fft input -> x
            x = np.zeros(cnt, dtype=int)
            for i in range(cnt):
                x[i] = mic[i]

            # 傅里叶变换
            freq_sig = np.abs(fftpack.fft(x) * 2 * np.pi / 128)
            freqs = fftpack.fftfreq(len(x)) * hz

            # print(_freq, _freq_sig)

            _len = int(len(freqs) / 2)  # 截半
            _freq = list(freqs[:_len])  # X
            _freq_sig = list(freq_sig[:_len])  # Y

            _is_change = True

            return "success"

        except Exception as e:
            print(e)
        return "fail"
    elif request.method == "GET":
        # 返回频谱图数据
        # data = {"x": ','.join(map(str, _freq)), "y": ','.join(map(str, _freq_sig))}
        json_data = jsonify({"x": jsonify(_freq).get_json(), "y": jsonify(_freq_sig).get_json(), "is_change": str(1 if _is_change else 0)})
        _is_change = False
        return json_data


@ app.route("/")
@ app.route("/index")
def index():
    # return 'hello'
    return render_template("index.html")


# RTMP
# localhost:5000
if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    app.run('0.0.0.0', port=5000)
# http://uykweb.ifast3.vipnps.vip/
