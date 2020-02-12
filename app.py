# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello Python!'

@app.route('/hc')
def health_check():
    return jsonify(message='The app is up and running'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='The resource was not found'), 404


@app.route('/books')
def books():
    name = request.args.get('name') 
    title = request.args.get('title') 
    page = int(request.args.get('total_pages')) 
    return jsonify(message='Book name: '+ name + ' Book Title: '+ title +' Total Pages: '+str(page)), 200

if __name__ == '__main__':
    app.run()
