"""Main Entrypoint for the Application"""

import logging
import json
import base64

from flask import Flask, request
from flask import jsonify

import Capitals
import utility


app = Flask(__name__)


@app.route('/')
def default():
    """Capital Idea!"""
    return 'Capital Idea!'

@app.route('/api/status', methods=['GET'])
def status():
    data = {
             "insert": True,
             "fetch": True,
             "delete": True,
             "list": True
           }
    return jsonify(data), 200

# @app.route('/api/capitals/<id>', methods=['POST'])
# def pubsub_receive():
#     """dumps a received pubsub message to the log"""

#     data = {}
#     try:
#         obj = request.get_json()
#         utility.log_info(json.dumps(obj))

#         data = base64.b64decode(obj['message']['data'])
#         utility.log_info(data)

#     except Exception as e:
#         # swallow up exceptions
#         logging.exception('Oops!')

#     return jsonify(data), 200


@app.route('/api/capitals', methods=['GET'])
def list_capitals():
    if request.method == 'GET':
        """Lists the names of capitals in the datastore"""
        caplist = Capitals.Capitals()

        results = caplist.fetch_capitals()
    return jsonify(results), 200

@app.route('/api/capitals/<int:capital_id>', methods=['GET', 'PUT'])
def get_by_id(capital_id):
    
    if request.method == 'GET':
        """Returns a single capital by its unique identifier"""
        caplist = Capitals.Capitals()
        capital = caplist.get_capital(capital_id)
        if not capital:
            return "Capital not found", 404
        return jsonify(capital), 200
           
    elif request.method == 'PUT':
        try:
            obj = request.get_json()
            caplist = Capitals.Capitals()
            caplist.store_capital(obj)
            return "Successfully stored the capital!", 200
        except Exception as e:
    return "Uknown error", 500

@app.route('/api/capitals/<capId>', methods=['DELETE'])
def delete_capital(capId):
    cap = Capitals.Capitals()
    try:
        cap.delete_capital(capId)
        return "", 200
    except Exception as e:
        return "Capital not found", 404


# @app.route('/notes', methods=['POST', 'GET'])
# def access_notes():
#     """inserts and retrieves notes from datastore"""

#     book = notebook.NoteBook()
#     if request.method == 'GET':
#         results = book.fetch_notes()
#         result = [notebook.parse_note_time(obj) for obj in results]
#         return jsonify(result)
#     elif request.method == 'POST':
#         print json.dumps(request.get_json())
#         text = request.get_json()['text']
#         book.store_note(text)
#         return "done"


@app.errorhandler(500)
def server_error(err):
    """Error handler"""
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)
