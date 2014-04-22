from flask import Flask, url_for, redirect, request, jsonify
from flask import request
from flask.ext.cors import cross_origin

from classify_instance import *

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/classify', methods=['GET'])
@cross_origin()
def getRating():
    patient_id = int(request.args.get('patient_id'))
    #instance_values = [1,2]
    #classification = classify(instance_values)
    response = {"classification": '?', "patient_id" : patient_id}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5002)
