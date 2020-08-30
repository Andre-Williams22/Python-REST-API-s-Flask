from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/nice')
def hello_world():
    retJson = {
        'field1': 'life',
        'field2': 'love'}

    return jsonify(retJson)



if __name__ == "__main__":
    app.run()