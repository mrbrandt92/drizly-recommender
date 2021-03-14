#!/usr/bin/env python
import json
import re
from http import HTTPStatus
from src.main import processRecommendations
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/') #to be filled in
def health_check():
    return "I'm healthy!"

@app.route('/invocations', methods=['POST'])
def find_recommendations():

    try:
        user_data = request.get_json()
    except Exception as e:
        print(e)
        abort(400)

    if not is_acceptable(user_data): abort(400)

    print('successfully received data')
    print(user_data)
    user_id, user_id_hash = list(user_data.items())[0]

    if len(user_id_hash) > 1:
        print("Please only call one user_id_hash at a time")
        abort(400)

    response = processRecommendations(str(user_id_hash[0]))

    try:
        if response == {}:
            print('returning 204 status code')
            return '', HTTPStatus.NO_CONTENT
    except Exception as e:
        print(e)

    return json.dumps(response)


def is_acceptable(data):

    id_key  = 'user_id_hashes'
    must_have_keys = [id_key]

    missing_incoming_fields = [k for k in must_have_keys if k not in data.keys()]
    if missing_incoming_fields:
        print(f'missing fields from request : {missing_incoming_fields}')
        print(f'bad data : {data}')
        return False

    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
