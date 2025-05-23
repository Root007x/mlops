from flask import Flask, render_template, request

"""
It creates a Flask application instance.
The app instance is the WSGI application callable that the server will use to communicate with the application.
"""
app = Flask(__name__)

@app.route("/")
def welcome():
    return "<html><h1>Welcome to the flask course</h1></html>"

@app.route("/index", methods = ['GET'])
def welcome_index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/form", methods = ['GET','POST'])
def form():
    if request.method == 'POST' :
        # name = request.form['name']
        # return f"Hello {name}"
        pass
    return render_template("form.html")

@app.route("/submit", methods = ['GET','POST'])
def submit():
    if request.method == 'POST' :
        name = request.form['name']
        return f"Hello {name}"
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)