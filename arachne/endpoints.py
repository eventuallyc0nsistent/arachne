from flask import request, jsonify

def spider_endpoint(**lookup):
    print request.endpoint
    return jsonify(hello='world')
