class BaseException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
    def to_json(self):
        return {'msg': self.message}, self.code

class UserExist(BaseException):
    def __init__(self, username):
        message = 'User {} already exists'.format(username)
        super().__init__(message, 400)

class UserNotExist(BaseException):
    def __init__(self, username):
        message = 'User {} doesn\'t exist'.format(username)
        super().__init__(message, 400)

class WrongCredentials(BaseException):
    def __init__(self):
        message = 'Wrong credentials'
        super().__init__(message, 401)

class InternalError(BaseException):
    def __init__(self):
        message = 'Something went wrong'
        super().__init__(message, 500)

class AssociationExist(BaseException):
    def __init__(self, **kwargs):
        fields = ", ".join(["{}: {}".format(key, value) for key, value in kwargs.items()])
        message = 'Association {} already exists'.format(fields)
        super().__init__(message, 400)

class AssociationNotExist(BaseException):
    def __init__(self, **kwargs):
        fields = ", ".join(["{}: {}".format(key, value) for key, value in kwargs.items()])
        message = 'Association {} doesn\'t exist'.format(fields)
        super().__init__(message, 400)

class CheckpointExist(BaseException):
    def __init__(self, checkpoint_name):
        message = 'Checkpoint {} already exists'.format(checkpoint_name)
        super().__init__(message, 400)

class CheckpointNotExist(BaseException):
    def __init__(self, checkpoint_name):
        message = 'Checkpoint {} doesn\'t exist'.format(checkpoint_name)
        super().__init__(message, 400)

class CheckpointFieldNotExist(BaseException):
    def __init__(self, checkpoint_name, field_name):
        message = 'Checkpoint {} with field {} doesn\'t exist'.format(checkpoint_name, field_name)
        super().__init__(message, 400)