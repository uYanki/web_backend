# 内容: 模板

import re
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    context = {
        'id': 18,  # int
        'name': 'uyk',
        'favs': ['makelove', 'fuckbitch','playgame'],  # list
        'infos': {
            'sex': 'male',
            'age': 18
        }  # dict
    }
    return render_template('filter.html', **context)


if __name__ == "__main__":
    app.run(debug=True)
