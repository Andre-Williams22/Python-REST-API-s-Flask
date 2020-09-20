# ''' 
# Requirements:
# - Register a user
# - given each user 10 tokens 
# - allow user to store a sentence in our database for 1 token 
# - retrieve his stored sentence on our database for 1 token 
# ''' 

# from flask import Flask, jsonify, request 
# from flask_restful import Api, Resource 
# from pymongo import MongoClient
# import os 
# import bcrypt 

# app = Flask(__name__)
# api = Api(app)

# client = MongoClient("mongodb://db:27017")
# db = client.SentencesDatabase
# users= db['Users']

# class Register(Resource):
#     def post(self):
#         # get the posted user data by the user
#         postedData = request.get_json()

#         # get data 
#         username = postedData["username"]
#         password = postedData["password"]

#         # store data in db
#         # hash 
#         hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

#         # store username and pw into the database 
#         users.insert({
#             "Username":username,
#             "Password": hashed_pw,
#             "Sentence": "",
#             "Tokens": 6 # user gets 6 tokens for everytime they want to insert something into db 
#         })

#         retJson = {
#             "status": 200,
#             "msg": "You successfully signed up for the API"
#         }
#         return jsonify(retJson)

# def verifyPw(username, password):
#     hashed_pw = users.find({ 
#         "Username": username
#     })[0]["Password"]

#     if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
#         return True
#     else:
#         return False

# def countTokens(username):
#     tokens = users.find({
#         "Username":username
#     })[0]["Tokens"]
#     return tokens

# class Store(Resource):
#     def post(self):
#         # 1. get posted data
#         postedData = request.get_json()

#         # 2. read the data
#         username = postedData["username"]
#         password = postedData["password"]
#         sentence = postedData["sentence"]

#         # 3. verify the username pw match 
#         correct_pw = verifyPw(username, password)

#         if not correct_pw:
#             retJson = {
#                 "status": 302
#             }
#             return jsonify(retJson)
#         # 4. verify user has enough tokens 
#         num_tokens = countTokens(username)
#         if num_tokens <= 0:
#             retJson = {
#                 "status": 301
#             }
#             return jsonify(retJson)
#         # 5. store the sentence, take one token away and return 2000k
#         users.update({
#             "Username": username
#         }, {
#             "$set":{
#                 "Sentence": sentence,
#                 "Tokens": num_tokens-1 
#             }
#         })

#         retJson = {
#             "status": 200, 
#             "msg": "Sentence saved successfully"
#         }
#         return jsonify(retJson)


# api.add_resource(Register, '/register')
# api.add_resource(Store, '/store')



# if __name__=='__main__':
#     app.run(host='0.0.0.0')