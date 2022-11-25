import os

from flask import Flask

from flask.views import View

app = Flask(__name__)
app.secret_key = "dev"


@app.route('/')
def index():
    pass


class RenderTemplateView(View):  # 类 django
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)


app.add_url_rule('/about', view_func=RenderTemplateView.as_view(
    'about_page', template_name='about.html'))


if __name__ == '__main__':
    app.run(debug=True)
