from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socket = SocketIO(app)

name_space = '/echo'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/push')
def broadcast_msg():  # 广播数据
    event_name = 'echo'
    broadcasted_data = {'data': "this message is boardcast!"}
    socket.emit(event_name, broadcasted_data, broadcast=True, namespace=name_space)
    return 'done!'


'''
基本流程: 无论时服务器，还是客户端，都需要通过函数 socket.on 将 event 绑定到函数上，以进行数据的双向传输
'''


@socket.on('connect', namespace=name_space)
def client_connected():  # 客户上线
    print('client connected.')
    socket.emit('echo', {'data': "hello!"}, broadcast=False, namespace=name_space)


@socket.on('disconnect', namespace=name_space)
def client_disconnect():  # 客户下线
    print('client disconnected.')


@socket.on('message', namespace=name_space)
def recv_msg(message):  # 接收消息
    print(message)
    socket.emit('echo', {'data': message['data']})  # 发送消息


if __name__ == "__main__":
    socket.run(app, host='127.0.0.1', port=5000, debug=True)
