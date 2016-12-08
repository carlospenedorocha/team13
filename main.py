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
            err = {
                    "code": 404,
                    "message": "Cannot fetch capital. Capital does not exist"
                }                
            return jsonify(err), 404
        return jsonify(capital[0]), 200
           
    elif request.method == 'PUT':
        try:
            obj = request.get_json()
            caplist = Capitals.Capitals()
            caplist.store_capital(obj)
            return "Successfully stored the capital!", 200
        except Exception as e:
            return "Uknown error", 500

@app.route('/api/capitals/<int:capId>', methods=['DELETE'])
def delete_capital(capId):
    cap = Capitals.Capitals()
    try:
        capital = cap.get_capital(capId)
        if not capital:
            err = {
                    "code": 404,
                    "message": "Cannot delete capital. Capital does not exist"
                }                
            return jsonify(err), 404

        cap.delete_capital(str(capId))
        return "", 200
        
    except Exception as e:
        err = {
                "code": 500,
                "message": e.message
            }                
        return jsonify(err), 500

@app.route('/api/capitals/<int:capId>/publish', methods=['POST'])
def pubsub_publish(capId):
    """publishes a capital"""

    cap = Capitals.Capitals()
    try:
        capital = cap.get_capital(capId)
        if not capital:
            err = {
                    "code": 404,
                    "message": "Capital record not found"
                }                
            return jsonify(err), 404

        obj = request.get_json()
        utility.log_info(json.dumps(obj))

        data = base64.b64decode(obj['message']['data'])
        utility.log_info(data)

        cap.publish_message(data["topic"], capital)
        return "", 200
        
    except Exception as e:
        err = {
                "code": 500,
                "message": e.message
            }                
        return jsonify(err), 500

    except Exception as e:
        # swallow up exceptions
        logging.exception('Oops!')

    return jsonify(data), 200

@app.route('/api/capitals/<int:capital_id>/store', methods=['POST'])
def store_capital_by_id(capital_id):
    """This method stores a capital to a file storage bucket by the capital's identifier."""
    try:
        caplist = Capitals.Capitals()
        capital = caplist.get_capital(capital_id)
        if not capital:
            err = {"code": 404, "message": "Capital record not found"}
            return jsonify(err), 404

        # Call file storage method
        success_message = {'messageId' : capital_id}

        return jsonify(success_message), 200
    except Exception as e:
        err = {"code": 500, "message": e.message}
        return jsonify(err), 500

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
