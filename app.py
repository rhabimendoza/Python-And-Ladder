# import flask and jinja
from flask import Flask, render_template, request, jsonify
import jinja2

# import lexical and syntax file
import lexical_file, syntax_file

# set jinja templates location
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader("template"))

# create app
app = Flask(__name__)

# route for /
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

# route for /documentation
@app.route("/documentation", methods=["GET", "POST"])
def documentation():
    return render_template("documentation.html")

# route for /analyze
@app.route("/analyze", methods=["GET", "POST"])
def lexical():
    return render_template("analyze.html")

# analyze code button is clicked
@app.route("/analyze_code", methods=["POST"])
def analyze_code():
    data = request.json
    code = data.get("code", "")
    lexical = ""
    syntax = ""
    if not code:
        lexical = ""
        syntax = ""
    else:
        lexical = lexical_file.lexical_function(code)
        syntax_li = syntax_file.parseInp()
        syntax = ""
        for s in syntax_li:
            syntax = syntax + s + "\n"
    return jsonify({"lexical": lexical, "syntax": syntax})