import pytest

from minimalweb import MinimalWeb, TextResponse

from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

BASE_URL = 'http://testserver'

@pytest.fixture
def app():
    return MinimalWeb()

@pytest.fixture
def client(app):
    session = RequestsSession()
    session.mount(prefix=BASE_URL, adapter=RequestsWSGIAdapter(app))
    return session

def test_basic_route(app):
    @app.route("/home")
    def home(req):
        return TextResponse("Home Page")

def test_route_overlap_throws_exception(app):
    @app.route("/home")
    def home(req):
        return TextResponse("Home Page")
    
    with pytest.raises(AssertionError):
        @app.route("/home")
        def home2(req):
            return TextResponse("Home Page")

def test_client_can_send_requests(app, client):
    EXPECTED_RESPONSE = "HELLO WORLD"

    @app.route("/helloworld")
    def helloworld(req):
        return TextResponse(EXPECTED_RESPONSE)

    assert client.get(BASE_URL + "/helloworld").text == EXPECTED_RESPONSE

def test_parameterized_handlers(app, client):
    @app.route("/hey/<string:name>")
    def hey(req, name):
        return TextResponse("Hello " + name)

    assert client.get(BASE_URL + "/hey/shahriar").text == "Hello shahriar"
    assert client.get(BASE_URL + "/hey/user2").text == "Hello user2"

def test_default_404_response(app, client):
    response = client.get(BASE_URL + "/something")
    
    assert response.status_code == 404
    assert response.text == "Page Not Found!"



