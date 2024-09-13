import sys
sys.path.append('.')
import pytest

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
