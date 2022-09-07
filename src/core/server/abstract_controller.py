from flask import jsonify
from src.core.server.instance import server

class AbstractController():

    def response(status, message, response_body_name=False, response_body=False):
        result = {}
        result['message'] = message

        if(response_body_name and response_body):
            result[response_body_name] = response_body
        
        return jsonify(result), status
