import os


class BaseError(Exception):

    def __init__(self, response):
        self.status_code = response.status_code
        resp = response.json()
        self.message = resp.get("message")
        self.parameters = resp.get("parameters")
        self.code = resp.get("code")
        self.errors = resp.get("errors")
        self.trace = resp.get("trace")
        super().__init__(self.message)

    def get_status_code(self):
        return self.status_code

    def get_parameters(self):
        return self.parameters

    def get_errors(self):
        return self.errors

    def get_code(self):
        return self.code

    def get_trace(self):
        return self.trace

    def get_message(self):
        return self.message

    def __repr__(self):
        return self.message


class BadRequestError(BaseError):
    def __init__(self, response):
        super().__init__(response)


class UnauthorizedError(BaseError):
    def __init__(self, response):
        super().__init__(response)


class UnexpectedError(BaseError):
    def __init__(self, response):
        super().__init__(response)
