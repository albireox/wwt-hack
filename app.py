from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def main():
    output = {'title': 'hello'}
    return render_template('index.html', **output)


app.run(debug=True)

