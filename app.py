from api import API
from middleware import Middleware


app = API()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/tell/{age:d}")
def tell_age(request, response, age):
    response.text = f"Hi, you mentioned that you are {age} years old"


@app.route("/book")
class BookResource:
    def get(self, req, resp):
        resp.text = "Books page"


@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template("index.html", context={"name": "bumbo", "title": "Best framework"}).encode()


@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be user")


def handler1(req, resp):
    resp.text = "YOLO"


def handler2(req, resp):
    resp.text = "YOLO"


app.add_route("/home1", handler1)
app.add_route("/home2", handler2)


def custom_exception_handler(request, response, exception_cls):
    response.text = "Oops! Something went wrong. Please contact our customer support."

app.add_exception_handler(custom_exception_handler)


class LoggingCustomMiddleware(Middleware):
    def process_request(self, req):
        print(f"Processing request: {req.url}")

    def process_response(self, req, resp):
        print(f"Processing response for request : {req.url}")

app.add_middleware(LoggingCustomMiddleware)
