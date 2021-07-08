from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/about/<username>')
def about_page(username):
    return f'<h1>Wellcome {username}</h1>'


@app.route('/anuraj')
def anuraj():
    return "This is me Mario"


if __name__ == "__main__":
    app.run(debug=True)
