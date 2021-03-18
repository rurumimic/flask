from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource, reqparse, fields

from pet import random_age, Pet

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0.0', title='SIMPLE API', description='this is simple api')
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

# Namespaces
fruit = api.namespace('fruit', description='my fruits')
animal = api.namespace('animal', description='my animals')

model = api.model('Pet', {
    'name': fields.String(required=True, readonly=True, description='Pet Name'),
    'age': fields.Integer(required=True, description='Pet Age')
})

parser = reqparse.RequestParser()
parser.add_argument('time', type=int, help='what time is it: 00')

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@fruit.route('/apple')
class FruitApple(Resource):
    def get(self):
        args = parser.parse_args()
        print(args)
        return {'fruit': 'apple'}

@fruit.route('/banana/<int:count>')
@fruit.param('count', 'how many')
class FruitBanana(Resource):
    def get(self, count):
        return {'fruit': 'banana', 'count': count}

@animal.route('/cat')
class AnimalCat(Resource):
    def get(self):
        return {'animal': 'cat', 'age': random_age() }

@animal.route('/pet')
class AnimalPet(Resource):
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
        body = request.json
        args = parser.parse_args()
        print(args)
        return Pet(name=body['name'], age=body['age'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
