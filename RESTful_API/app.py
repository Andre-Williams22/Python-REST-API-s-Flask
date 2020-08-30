from flask import Flask, jsonify, request 
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


def checkPostedData(postData, functionName):
    if functionName == "add":
        if "x" not in postData or "y" not in postData:
            return 301 # means there's a missing parameter
        else:
            return 200
    
class Add(Resource):
    def post(self):
        # resource add requested POST
        #1. get posted data 
        postedData = request.get_json()

        # step 1.5 verify validity of posted data 
        status_code = checkPostedData(postedData, "add")
        if status_code!=200:
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        # if I'm here then status_code == 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # 2. add the posted data
        tot = x+y
        retMap = {
            'Sum': tot,
            'Status Code': 200
        }
        return jsonify(retMap)


class Subtract(Resource):
    pass

class Divide(Resource):
    pass

class Multiply(Resource):
    pass

api.add_resource(Add, "/add")

@app.route('/')
def hello_world():
    return 'Hello Andre'



if __name__ == "__main__":
    app.run()