# MinimalWeb
MinimalWeb is a Python Web Framework based on WSGI. It's just for ones that like to learn about implementing a web framework from scratch.

## Course
You can watch the course behind this framework on youtube from [here](https://www.youtube.com/playlist?list=PLRU2zoAmuzJ33x-___WkhyTJ8dDPaoOPk). videos are in Persian (Farsi) language.

## How To Setup
1. Install Python v3.9 or later.
2. Install virtualenv:
```bash
pip insatll virtualenv
```
3. Create a virtual environment:
```bash
virtualenv venv
```
4. Active the virtual environment (On UNIX):
```bash
source venv/bin/activate
```
5. Install all the requirements by using this command:
```bash
pip install -r requirements.txt
```

## Quick Sample
```python
from minimalweb import MinimalWeb, TextResponse, HtmlResponse

app = MinimalWeb()

# Render html using Jinja2
@app.route("/")
def index(req):
    context = {
        "users": ["user1", "user2"]
    }
    return HtmlResponse("index.html", context=context)
    
# Using Url Args
@app.route("/user/<string:username>")
def user(req, username):
    return TextResponse(f"Hello, {username}")

# Start app
app.run()
```

## More Options
* Serving static and dynamic files.
* Adding custom middlewares.
* Running web app without alternative web servers.

## Contribution
Feel free to contribute to this project :)

