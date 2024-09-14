from api import API


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


def handler1(req, resp):
    resp.text = "YOLO"


def handler2(req, resp):
    resp.text = "YOLO"


app.add_route("/home1", handler1)
app.add_route("/home2", handler2)

