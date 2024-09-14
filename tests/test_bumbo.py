import sys
sys.path.append('.')
import pytest


test_server_base_url = "http://testserver"


def test_basic_route(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "YOLO"


def test_route_overlap_throws_exception(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(ValueError):
        @app.route("/home")

        def home2(req, resp):
            resp.text = "YOLO again"


def test_bumbo_test_client_can_send_requests(app, client):
    expected_response_text = "Hello World!"

    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello World!"

    assert expected_response_text == client.get(test_server_base_url+"/home").text


def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"Hi, {name}"

    assert "Hi, Sid" == client.get(test_server_base_url+"/Sid").text
    assert "Hi, Trisha" == client.get(test_server_base_url+"/Trisha").text


def test_default_404_response(client):
    response = client.get(test_server_base_url+"/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not found."


def test_class_handler_get_method(app, client):
    expected_response = "test book page"
    @app.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = expected_response

    assert client.get(test_server_base_url+"/book").text == expected_response


def test_alternative_route_django_style(app, client):
    expected_response_text = "Alternative way to add a route"

    def home(req, resp):
        resp.text = expected_response_text

    app.add_route("/alternative", home)

    assert client.get(test_server_base_url+"/alternative").text == expected_response_text
