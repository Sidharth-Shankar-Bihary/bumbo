from webob import Request, Response
from parse import parse
import inspect
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
import os
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
from middleware import Middleware


class API:
    def __init__(self, templates_dir="templates", static_dir="static"):
        self.routes = dict()
        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)
        self.middleware = Middleware(self)

    def add_route(self, path, handler):
        if path in self.routes:
            raise ValueError("Such route already exists.")
        
        self.routes[path] = handler


    def route(self, path):
        if path in self.routes:
            raise ValueError("Such route already exists.")

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper
    
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        
        response = self.handle_request(request) 

        return response(environ, start_response)
        
    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]

        if path_info.startswith("/static"):
            environ["PATH_INFO"] = path_info[len("/static"):]
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)
        try:
            if handler is not None:
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError("Method not allowed", request.method)
                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as ex:
            if self.exception_handler is None:
                raise ex
            else:
                self.exception_handler(request, response, ex)

        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = dict()

        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
