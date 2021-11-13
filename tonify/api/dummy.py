from flask import request
from flask.ext.restful import Resource, Api, marshal_with, fields, abort
from flask_restful_swagger import swagger
from .models import DummyResult
from .models import HelloResult
from .models import SendMessagesResult
from .errors import JsonRequiredError
from .errors import JsonInvalidError

class DummyEndpoint(Resource):
    @swagger.operation(
        responseClass=DummyResult.__name__,
        nickname='dummy')
    @marshal_with(DummyResult.resource_fields)
    def get(self):
        """Return a DummyResult object

        Lightweight response to let us confirm that the server is on-line"""
        return DummyResult()


class HelloEndpoint(Resource):
    @swagger.operation(
        responseClass=HelloResult.__name__,
        nickname='hello',
        responseMessages=[
            {"code": 400, "message": "Input required"},
            {"code": 500, "message": "JSON format not valid"},
        ],
        parameters=[
            {
                "name": "name",
                "description": "JSON-encoded name",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            },
        ])
    @marshal_with(HelloResult.resource_fields)
    def post(self):
        """Return a HelloResult object"""
        reqs = request.get_json()
        if not reqs:
            raise JsonRequiredError()
        try:
            reqs['name']
            return HelloResult(name=reqs['name'])
        except KeyError:
            raise JsonInvalidError()

class SendMessagesEndpoint(Resource):
    @swagger.operation(
        responseClass=SendMessagesResult.__name__,
        nickname='send',
        responseMessages=[
            {"code": 400, "message": "Input required"},
            {"code": 500, "message": "JSON format not valid"},
        ],
        parameters=[
            {
                "name": "name",
                "description": "JSON-encoded name",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "body"
            },
        ])
    @marshal_with(SendMessagesResult.resource_fields)
    def post(self):
        """Return a SendMessagesResult object"""
        # dictionary with key 'messages' of list of dictionaries of date, author, message 
        reqs = request.get_json()        

        if not reqs:
            raise JsonRequiredError()
        
        try:
            reqs = reqs[1]
            
            res = processMessages(reqs)

            return SendMessagesResult(tones=res)
        except KeyError:
            raise JsonInvalidError()

def processMessages(reqs):
    return [
        {'srs': 1, 'j': 0},
        {'srs': 0.5, 'j': 0.3},
    ]