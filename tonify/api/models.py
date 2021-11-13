from flask.ext.restful import Resource, Api, marshal_with, fields, abort
from flask_restful_swagger import swagger

@swagger.model
class DummyResult(object):
    """The result of a call to /dummy"""
    resource_fields = {
        'dummy': fields.String
    }

    def __init__(self):
        self.dummy = "foobar"


@swagger.model
class HelloResult(object):
    """The result of a call to /hello"""
    resource_fields = {
        'greetings': fields.String
    }

    def __init__(self, name):
        self.greetings = "Hello {}".format(name)

@swagger.model
class SendMessagesResult(object):
    """The result of a call to /send"""
    resource_fields = {
        'tones': fields.List(
            fields.Raw(
                fields.Nested({
                    'srs': fields.Float,
                    'j': fields.Float,
                })
            )
        )
    }

    def __init__(self, tones):
        self.tones = tones
