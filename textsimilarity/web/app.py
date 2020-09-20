from flask import Flask, jsonify, request 
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt 
import spacy


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB 
users = db["Users"]

def UserExist(username):
    if users.find({"Username": username}).count() == 0:
        return False 
    else:
        return True

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)
        
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6 # six tokens until they have to pay
        })

        retJson = {
            "status": 200,
            "msg": "You've successfully signed up to the API"
        }
def verifyPw(username, password):
    if not UserExist(username):
        return False 

    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw)==hashed_pw:
        return True
    else:
        return False 

def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens 

class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not UserExist(username):
            retJson = {
                "status": "301",
                "msg": "Invalid Username"
            }
            return jsonify(retJson)

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "msg" : "Invalid Password"
            }

        num_tokens = countTokens(username)
        
        if num_tokens <= 0:
            retJson = {
                "status": 303,
                "msg": "Sorry you're out of tokens, please refill!"
            }

            return jsonify(retJson)

        # calculate the edit distance
        nlp = spacy.load('en_core_web_sm') # load in spacy 

        text1 = nlp(text1)
        text2 = nlp(text2)
        # ratio is num between 0 to 1 and the closer to 1, the more similar text1 and text2 are
        ratio = text1.similarity(text2)

        retJson = {
            "status": 200,
            "similarity": ratio,
            "msg": "Similarity score calculated successfully"

        }
        # subtract token from our user 

        current_tokens = countTokens(username)

        users.update({
            "Username": username,
        },{
            "$set": {
                "Tokens": current_tokens-1
            }
        })

        return jsonify(retJson)



@app.route('/')
def hellow_world():
    return "hello world!"
