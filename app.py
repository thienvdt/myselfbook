from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello Python!'


@app.route('/super_simple')
def super_simple():
    return 'Hello from the Planetary API.'


@app.route('/hc')
def health_check():
    return jsonify(message='The app is healthy and running ☺')


if __name__ == '__main__':
    app.run()
