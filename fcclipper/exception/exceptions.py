""" Exceptions Module """

class FcclipperInternalException(Exception):
    """ Internal fcclipper Exception """

    def __init__(self, message, error_code=None):
        """ FcclipperInternalException constructor """
        self.message = message
        self.error_code = error_code
        super().__init__(message, error_code)

    def __str__(self):
        if self.error_code:
            return f'FcclipperInternalException: {self.message}  Error Code: {str(self.error_code)}'
        return f'FcclipperInternalException: {self.message}'
