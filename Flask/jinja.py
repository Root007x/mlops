### Jinja2 Template Engine
"""
{{ }} expression to print the value of a variable
{% %} expression to execute a statement
{# #} comment
"""

from flask import Flask, render_template, request, redirect, url_for

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

# @app.route("/submit", methods = ['GET','POST'])
# def submit():
#     if request.method == 'POST' :
#         name = request.form['name']
#         return f"Hello {name}"
#     return render_template("form.html")

## Variable Rules
@app.route("/success/<int:score>")
def success(score):
    res =""
    if score >= 50:
        res = "PASS"
    else:
        res = "FAIL"
    
    return render_template("result.html",results = res)

## Variable Rules
@app.route("/successres/<float:score>")
def success_res(score):
    res =""
    if score >= 50:
        res = "PASS"
    else:
        res = "FAIL"
    
    exp = {
        "score": score,
        "result": res
    }
    
    return render_template("result1.html",results = exp)

## if condition
@app.route("/successif/<int:score>")
def successif(score):    
    return render_template("result.html",results = score)

## Dynamic URL
@app.route("/fail/<int:score>")
def fail(score):
    return render_template("result.html",results = score)

@app.route("/submit", methods = ['GET','POST'])
def submit():
    total_score = 0
    if request.method == "POST":
        science = float(request.form["science"])
        maths = float(request.form["maths"])
        c = float(request.form["c"])
        data_science = float(request.form["datascience"])

        total_score = (science + maths + c + data_science)/4
    else:
        return render_template('getresult.html')
    
    return redirect(url_for('success_res', score = total_score))
 
if __name__ == "__main__": 
    app.run(debug=True)