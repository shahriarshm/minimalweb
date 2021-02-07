import os

from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed
from werkzeug.wrappers import Request, Response

from jinja2 import Environment, FileSystemLoader

from middleware import BaseMiddleware

import inspect

class TextResponse(Response):
    pass

class HtmlResponse(Response):
    def __init__(self, template_name, templates_dir="templates", context=None):
        if context is None:
            context = {}

        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))
        text = self.templates_env.get_template(template_name).render(**context)

        super(HtmlResponse, self).__init__(text, content_type="text/html")

class MinimalWeb():
    def __init__(self):
        self.routes = {}
        self.url_rules = Map()

        self.middleware = BaseMiddleware(self)

    def __call__(self, environ, start_response):
        return self.middleware(environ, start_response)
    
    # No longer need
    # def wsgi_app(self, environ, start_response):
    #     request = Request(environ)
    #     response = self.dispatch_request(request)
    #     return response(environ, start_response)

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
    
    def dispatch_request(self, request):
        adapter = self.url_rules.bind_to_environ(request.environ)
        try:
            endpoint, kwargs = adapter.match()
            handler = self.routes[endpoint]
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                assert handler is not None, f"Method not exists in {endpoint}."

            return handler(request, **kwargs)
        except NotFound:
            return self.error_404(request)
        except MethodNotAllowed:
            return self.error_405(request)
        except HTTPException as e:
            return e

    def error_404(self, request):
        return TextResponse("Page Not Found!", status=404)

    def error_405(self, request):
        return TextResponse("Method not allowed!", status=405)

    def check_route_exists(self, path, endpoint):
        if endpoint in self.routes:
            return True
        for rule in self.url_rules.iter_rules():
            if rule.rule == path:
                return True
        return False

    def route(self, path, methods=None):
        def wrapper(handler):
            endpoint = handler.__name__
            assert not self.check_route_exists(path, endpoint), "Method already exists."
            rule = Rule(path, endpoint=endpoint, methods=methods)
            self.routes[endpoint] = handler
            self.url_rules.add(rule)
            return handler
        return wrapper
            

