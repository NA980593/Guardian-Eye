from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Home Page<h1>"

if __name__ == 'main':
    app.run(debug = True)