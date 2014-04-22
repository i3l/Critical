from flask import Flask, url_for, redirect, request, jsonify
from flask import request
from flask.ext.cors import cross_origin

from classify_instance import *

from 

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/classify', methods=['GET'])
@cross_origin()
def getRating():
    url = int(request.args.get('patient_id'))
    response = {status:"1"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port = 5003)
