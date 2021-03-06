

error_messages = {
    'JsonRequestParsingError': {
        'message': "Error during request data parsing.",
        'status': 400,
        'extra': "Check your JSON syntax.",
    },
    'RequestDataError': {
        'message': "Error during request data parsing.",
        'status': 400,
        'extra': "Check for missing data fields.",
    },
    'RequestError': {
        'message': "Error during request execution.",
        'status': 400,
    },
    'ResourceAlreadyExistsError': {
        'message': "A resource with that UUID already exists.",
        'status': 409,
    },
    'ResourceNotFoundError': {
        'message': "A resource with that UUID does not exist.",
        'status': 404,
    },
}


class JsonRequestParsingError(Exception):
    pass


class RequestDataError(Exception):
    pass


class RequestError(Exception):
    pass


class ResourceAlreadyExistsError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass
