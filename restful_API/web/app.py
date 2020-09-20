
from flask import Flask, jsonify, request 
from flask_restful import Api, Resource 
from pymongo import MongoClient
import os 
import bcrypt 


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users= db['Users']


''' 
Requirements:
- Register a user
- given each user 10 tokens 
- allow user to store a sentence in our database for 1 token 
- retrieve his stored sentence on our database for 1 token 
''' 


class Register(Resource):
    def post(self):
        # get the posted user data by the user
        postedData = request.get_json()

        # get data 
        username = postedData["username"]
        password = postedData["password"]

        # store data in db
        # hash 
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # store username and pw into the database 
        users.insert({
            "Username":username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 6 # user gets 6 tokens for everytime they want to insert something into db 
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

def verifyPw(username, password):
    hashed_pw = users.find({ 
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]
    return tokens
    
class Store(Resource):
    def post(self):
        # 1. get posted data
        postedData = request.get_json()

        # 2. read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        # 3. verify the username pw match 
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)
        # 4. verify user has enough tokens 
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)
        # 5. store the sentence, take one token away and return 2000k
        users.update({
            "Username": username
        }, {
            "$set":{
                "Sentence": sentence,
                "Tokens": num_tokens-1 
            }
        })

        retJson = {
            "status": 200, 
            "msg": "Sentence saved successfully"
        }
        return jsonify(retJson)


class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
            
        # verify username password
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)


        # make user pay! 
        users.update({
            "Username": username
        }, {
            "$set":{
                "Tokens": num_tokens-1  # decrease their num of tokens
                }
        })


        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "sentence": sentence
        }

        return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)









# from flask import Flask, jsonify, request 
# from flask_restful import Api, Resource
# from pymongo import MongoClient

# app = Flask(__name__)
# api = Api(app)

# client = MongoClient("mongodb://db:27017")
# db = client.aNewDB
# UserNum = db["UserNum"]

# UserNum.insert({
#     'num_of_users':0
# })

# class Visit(Resource):
#     def get(self):
#         prev_num = UserNum.find({})[0]['num_of_users']
#         new_num = prev_num + 1 
#         UserNum.update({}, {"$set":{"num_of_users": new_num}})
#         return str("Hello user " + str(new_num))


# def checkPostedData(postData, functionName):
#     if functionName == "add" or functionName == "subtract" or functionName =='multiply':
#         if "x" not in postData or "y" not in postData:
#             return 301 # means there's a missing parameter
#         else:
#             return 200
#     elif functionName == 'divide':
#         if 'x' not in postData or 'y' not in postData:
#             return 301
#         elif int(postData['y']) ==0:
#             return 302
#         else:
#             return 200
    
# class Add(Resource):
#     def post(self):
#         # resource add requested POST
#         #1. get posted data 
#         postedData = request.get_json()

#         # step 1.5 verify validity of posted data 
#         status_code = checkPostedData(postedData, "add")
#         if status_code!=200:
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code": status_code
#             }
#             return jsonify(retJson)

#         # if I'm here then status_code == 200
#         x = postedData['x']
#         y = postedData['y']
#         x = int(x)
#         y = int(y)

#         # 2. add the posted data
#         tot = x+y
#         retMap = {
#             'Sum': tot,
#             'Status Code': 200
#         }
#         return jsonify(retMap)


# class Subtract(Resource):
#     def post(self):
#         # resource subtract requested with POST
#         #1. get posted data 
#         postedData = request.get_json()

#         # step 1.5 verify validity of posted data 
#         status_code = checkPostedData(postedData, "subtract")
#         if status_code!=200:
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code": status_code
#             }
#             return jsonify(retJson)

#         # if I'm here then status_code == 200
#         x = postedData['x']
#         y = postedData['y']
#         x = int(x)
#         y = int(y)

#         # 2. add the posted data
#         tot = x-y
#         retMap = {
#             'Sum': tot,
#             'Status Code': 200
#         }
#         return jsonify(retMap)

# class Divide(Resource):
#     def post(self):
#         # resource subtract requested with POST
#         #1. get posted data 
#         postedData = request.get_json()

#         # step 1.5 verify validity of posted data 
#         status_code = checkPostedData(postedData, "divide")
#         if status_code!=200:
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code": status_code
#             }
#             return jsonify(retJson)

#         # if I'm here then status_code == 200
#         x = postedData['x']
#         y = postedData['y']
#         x = int(x)
#         y = int(y)

#         # 2. add the posted data
#         tot = (x*1.0)/y
#         retMap = {
#             'Sum': tot,
#             'Status Code': 200
#         }
#         return jsonify(retMap)

# class Multiply(Resource):
#     def post(self):
#         # resource subtract requested with POST
#         #1. get posted data 
#         postedData = request.get_json()

#         # step 1.5 verify validity of posted data 
#         status_code = checkPostedData(postedData, "multiply")
#         if status_code!=200:
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code": status_code
#             }
#             return jsonify(retJson)

#         # if I'm here then status_code == 200
#         x = postedData['x']
#         y = postedData['y']
#         x = int(x)
#         y = int(y)

#         # 2. add the posted data
#         tot = x*y
#         retMap = {
#             'Sum': tot,
#             'Status Code': 200
#         }
#         return jsonify(retMap)
# api.add_resource(Add, "/add")
# api.add_resource(Subtract, "/subtract") 
# api.add_resource(Multiply, "/multiply")
# api.add_resource(Divide, "/divide")
# api.add_resource(Visit, "/hello")
# @app.route('/')
# def hello_world():
#     return 'Hello Andre'


# # docker build -t dockerpython .
# # docker run -p 5000:5000 dockerpython

# # sudo docker-compose build 
# # sudo docker-compose up

# # In Vagrant on VM 
# # flask run --host=0.0.0.0
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)