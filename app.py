from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>Welcome to Movie DB test</title>
        </head>
        <body style="background-color: #131410;">
            <h1 style="color: #F5F6ED; text-align: center;">Welcome to Movie DB</h1>
        </body>
    </html>
    """

