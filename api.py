from webob import Request, Response


class API:
    def __init__(self):
        self.routes = dict()

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def __call__(self, environ, start_response):
        request = Request(environ)
        
        response = self.handle_request(request) 

        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()

        handler = self.find_handler(request_path=request.path)
        handler(request, response)

        return response

    def find_handler(self, request_path):
        return self.routes.get(request_path, self.default_response)

    def default_response(self, request, response):
        response.status_code = 404
        response.text = "Not found."
