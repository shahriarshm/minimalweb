from werkzeug.wrappers import Request

class BaseMiddleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.app.dispatch_request(request)
        return response(environ, start_response)

    def dispatch_request(self, request):
        request = self.process_request(request)
        response = self.app.dispatch_request(request)
        response = self.process_response(response)
        return response

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass
