from flask import Flask, jsonify, request 

app = Flask(__name__)


@app.route('/')
def hellow_world():
    return "hello world!"

@app.route('/add_two_nums', methods=['POST'])
def add_two_nums():
    # get x,y from the posted data 
    dataDict = request.get_json()

    if "x" not in dataDict:
        return "ERROR", 305

    x = dataDict["x"]
    y = dataDict["y"]

    z = x+y

    retJSON = { "z":z }

    
    return jsonify(retJSON), 200
    # add z=x+y
    # prepare a JSON, "z":z
    # 
    # 
    # return jsonify(map_prepared) 

@app.route('/nice')
def nice():
    retJson = {
        'field1': 'life',
        'field2': 'love'}

    return jsonify(retJson)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)