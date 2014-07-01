

error_messages = {
    'JsonRequestParsingError': {
        'message': "Error during request data parsing.",
        'status': 400,
        'extra': "Check your JSON syntax.",
    },
    'UeAlreadyExistsError': {
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

class ResourceAlreadyExistsError(Exception):
    pass

class ResourceNotFoundError(Exception):
    pass