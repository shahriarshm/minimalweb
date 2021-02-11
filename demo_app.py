from minimalweb import MinimalWeb, TextResponse, HtmlResponse
from middleware import BaseMiddleware

app = MinimalWeb()

class MyMiddleware(BaseMiddleware):
    def process_request(self, req):
        print("FROM Middleware 1 Processing req", req.url)
        return req

    def process_response(self, req, res):
        print("FROM Middleware 1 Processing res", req.url)
        return res

class MyMiddleware2(BaseMiddleware):
    def process_request(self, req):
        print("FROM Middleware 2 Processing req", req.url)
        return req

    def process_response(self, req, res):
        print("FROM Middleware 2 Processing res", req.url)
        return res

app.add_middleware(MyMiddleware)
app.add_middleware(MyMiddleware2)

app.serve_files()

@app.route("/")
def index(req):
    # Testing Context
    context = {
        "id": 1,
        "name": "Shahriar",
        "users": ["user1", "user2"]
    }
    return HtmlResponse("index.html", context=context)

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