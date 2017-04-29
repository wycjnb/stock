from flask import Flask, render_template
from flask_restful import Api, Resource

from server import urls

app = Flask(__name__)
api = Api(app)




@app.route('/')
def test():
    return render_template('tests.html')

class HelloWorld(Resource):
    def get(self):
        return [{'name': 'a1', 'panel_id': 1}, {'name': 'a2', 'panel_id': 2}]

api.add_resource(HelloWorld, '/a1')

class HelloWorld1(Resource):
    def get(self):
        # return {'a': [1, 3, 3, 1, 2]}
        return [{'panel_id': 1, 'list': [1, 2]}, {'panel_id': 2, 'list': [2, 3]}]
api.add_resource(HelloWorld1, '/a2')


class HelloWorld2(Resource):
    def get(self):
        return [{'panel_id': 1, 'list': [{'a': 3, 'b': '002457', 'c': 1, 'd': 1, 'e': 1, 'f': 1}, {'a': 4, 'b': '000958', 'c': 1, 'd': 1, 'e': 1, 'f': 1}]},
                {'panel_id': 2, 'list': [{'a': 2, 'b': '002672', 'c': 1, 'd': 1, 'e': 1, 'f': 2}]}]

api.add_resource(HelloWorld2, '/a3')

if __name__ == '__main__':
    urls.add_resource(api)
    app.run(host='0.0.0.0', port=5000, debug=True)
