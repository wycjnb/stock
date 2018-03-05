from gevent import monkey
monkey.patch_all()
import gevent.wsgi
from flask import Flask, render_template
from flask_restful import Api, Resource

from server import urls

app = Flask(__name__)
api = Api(app)

app.jinja_env.variable_start_string = '[[ '
app.jinja_env.variable_start_string = ']] '

@app.route('/')
def test():
    return render_template('index.html')


if __name__ == '__main__':
    urls.add_resource(api)
	print(1111)
    server = gevent.wsgi.WSGIServer(('0.0.0.0', 80), app)
    server.serve_forever()
