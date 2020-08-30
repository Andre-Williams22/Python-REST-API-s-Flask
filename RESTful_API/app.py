from flask import Flask, jsonify, request 
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

class Add(Resource):
    def post(self):
        # resource add requested POST
        
    def get(self):
        # resource add was requested using GET


class Subtract(Resource):
    pass

class Divide(Resource):
    pass

class Multiply(Resource):
    pass


@app.route('/')
def hello_world():
    return 'Hello Andre'



if __name__ == "__main__":
    app.run()