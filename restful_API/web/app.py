from flask import Flask, jsonify, request 
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1 
        UserNum.update({}, {"$set":{"num_of_users": new_num}})
        return str("Hello user " + str(new_num))


def checkPostedData(postData, functionName):
    if functionName == "add" or functionName == "subtract" or functionName =='multiply':
        if "x" not in postData or "y" not in postData:
            return 301 # means there's a missing parameter
        else:
            return 200
    elif functionName == 'divide':
        if 'x' not in postData or 'y' not in postData:
            return 301
        elif int(postData['y']) ==0:
            return 302
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
    def post(self):
        # resource subtract requested with POST
        #1. get posted data 
        postedData = request.get_json()

        # step 1.5 verify validity of posted data 
        status_code = checkPostedData(postedData, "subtract")
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
        tot = x-y
        retMap = {
            'Sum': tot,
            'Status Code': 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        # resource subtract requested with POST
        #1. get posted data 
        postedData = request.get_json()

        # step 1.5 verify validity of posted data 
        status_code = checkPostedData(postedData, "divide")
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
        tot = (x*1.0)/y
        retMap = {
            'Sum': tot,
            'Status Code': 200
        }
        return jsonify(retMap)

class Multiply(Resource):
    def post(self):
        # resource subtract requested with POST
        #1. get posted data 
        postedData = request.get_json()

        # step 1.5 verify validity of posted data 
        status_code = checkPostedData(postedData, "multiply")
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
        tot = x*y
        retMap = {
            'Sum': tot,
            'Status Code': 200
        }
        return jsonify(retMap)
api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract") 
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/hello")
@app.route('/')
def hello_world():
    return 'Hello Andre'


# docker build -t dockerpython .
# docker run -p 5000:5000 dockerpython

# sudo docker-compose build 
# sudo docker-compose up

# In Vagrant on VM 
# flask run --host=0.0.0.0
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)