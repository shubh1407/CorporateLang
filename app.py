from flask import Flask, Response, render_template, request
import time
import os
from interpretator import run_program
app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    code = request.form["code"].splitlines()
    print("Running code:", code)
    #output = run_program(code)
    return Response(run_program(code), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port,debug=True)