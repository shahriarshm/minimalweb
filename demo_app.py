from minimalweb import MinimalWeb, TextResponse
from middleware import BaseMiddleware

app = MinimalWeb()

class MyMiddleware(BaseMiddleware):
    def process_request(self, req):
        print("Processing req", req.url)
        return req

    def process_response(self, req, res):
        print("Processing res", req.url)
        return res

app.add_middleware(MyMiddleware)

@app.route("/")
def index(req):
    if req.method == "GET":
        text = "GET Method"
    elif req.method == "POST":
        text = "POST Method"
    return TextResponse("Index Page! " + text)

@app.route("/detail", methods=["GET", "POST"])
class DetailView():
    def head(self, req):
        return TextResponse("")

    def get(self, req):
        return TextResponse("Detail View with GET method.")

    def post(self, req):
        return TextResponse("Detail View with POST method.")

@app.route("/user/<string:username>")
def user(req, username):
    return TextResponse(f"Hello, {username}")

@app.route("/movie/<int:mid>/<string:title>")
def movie(req, mid, title):
    return TextResponse(f"Found a movie by id {mid} and title {title}")

@app.route("/dashboard")
def dashboard(req):
    return TextResponse("Dashboard Page!")