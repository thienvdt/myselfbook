# -*- coding: utf8 -*-
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import date

import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'myselfbook.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('DB has been created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DB dropped!')


@app.cli.command('db_seed')
def db_seed():
    test_user = User(first_name='Alex', last_name='Vo', email='voduythien16392@gmail.com',
                     password='abc12345', username='thienvdt', created_date=date.today(), created_by='thienvdt')

    db.session.add(test_user)

    book = Book(name='Hai huoc mot chut, the gioi se khac di',
                description='hai hoc di nao...', created_date=date.today(), cover='Default_cover.png', created_by='thienvdt')
    book1 = Book(name='Bay nguyen tac hieu qua', description='bay nguyen tac cua thanh cong...',
                 created_date=date.today(), cover='Default_cover.png', created_by=0)

    db.session.add(book)
    db.session.add(book1)

    db.session.commit()
    print('Database seeded!')


@app.route('/')
def index():
    return 'Hello Python!'


@app.route('/hc')
def health_check():
    return jsonify(message='The app is up and running'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='The resource was not found'), 404


@app.route('/books', methods=['GET'])
def books():
    books = Book.query.all()
    result = book_schemas.dump(books)
    return jsonify(data=result)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_date = Column(DateTime)
    created_by = Column(String)


class UserBook(db.Model):
    __tablename__ = 'user_books'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    book_id = Column(Integer)
    status = Column(Integer)
    created_date = Column(DateTime)
    created_by = Column(String)


class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cover = Column(String)
    description = Column(String)
    created_date = Column(DateTime)
    created_by = Column(String)


class UserSchema(ma.Schema):
    class Meta:
        fields= ('id', 'first_name','last_name','email', 'password','created_date','created_by')
class UserBookSchema(ma.Schema):
    class Meta:
        fields= ('id', 'user_id','book_id','status', 'created_date','created_by')
class BookSchema(ma.Schema):
    class Meta:
        fields= ('id', 'name','cover','description', 'created_date','created_by')       
user_schema= UserSchema()
user_schemas= UserSchema(many=True)
user_book_schema= UserBookSchema()
user_book_schemas= UserBookSchema(many=True)
book_schema= BookSchema()
book_schemas= BookSchema(many=True)

if __name__ == '__main__':
    app.run()
