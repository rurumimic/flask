from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource, reqparse, fields

from pet import random_age, Pet
from food.food import Food

from pprint import pprint as pp

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0.0', title='SIMPLE API', description='this is simple api')
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

# Namespaces
fruit = api.namespace('fruit', description='my fruits')
animal = api.namespace('animal', description='my animals')
shop = api.namespace('shop', description='my shop')
mirror = api.namespace('mirror', description='reflect')

model = api.model('Pet', {
    'name': fields.String(required=True, readonly=True, description='Pet Name'),
    'age': fields.Integer(required=True, description='Pet Age')
})

parser = reqparse.RequestParser()
parser.add_argument('time', type=int, help='what time is it: 00')

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        print(request.args)
        name = request.args.get('name', default='empty')
        values = request.args.getlist('values')
        return {'hello': 'world', 'name': name, 'values': values}

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

@shop.route('/<string:name>')
@shop.param('name', 'apple')
class FoodShop(Resource):
    def get(self, name):
        food = Food()
        return food.catalog(name)

@mirror.route('/')
@mirror.doc(
    params = {
        'Header_Key': {'in': 'header', 'default': 'value', 'schema': {'type': 'string'}, 'description': 'value'},
        'key': {'in': 'query', 'default': 'value', 'schema': {'type': 'string'}, 'description': 'value'},
    }
)
class Mirror(Resource):
    def get(self):
        headers = {k:v for k, v in request.headers.items()}
        args = request.args.to_dict()
        return {
            'headers': headers,
            'args': args
        }
    
    @api.expect(model)
    def post(self):
        headers = {k:v for k, v in request.headers.items()}
        args = request.args.to_dict()
        return {
            'headers': headers,
            'args': args,
            'data': request.json,
        }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
