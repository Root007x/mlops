from flask import Flask, render_template

"""
It creates a Flask application instance.
The app instance is the WSGI application callable that the server will use to communicate with the application.
"""
app = Flask(__name__)

@app.route("/")
def welcome():
    return "<html><h1>Welcome to the flask course</h1></html>"

@app.route("/index")
def welcome_index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
