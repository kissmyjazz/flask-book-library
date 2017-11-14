import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from healthcheck import HealthCheck, EnvironmentDump
from security import authenticate, identity
from resources.user import UserRegister
from resources.customer import Customer, CustomerList, CustomerListofBooks
from resources.book import Book, BookList, BorrowedBookList, AvailableBookList, BorrowBook, ReturnBook

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 30 # 30 min
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///denis')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'denis'
api = Api(app)

# wrap the flask app and give a heathcheck url
health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment")

jwt = JWT(app, authenticate, identity)

api.add_resource(BookList, '/books/')
api.add_resource(Book, '/books/<string(minlength=10, maxlength=13):isbn>', endpoint="api.book_details")
api.add_resource(BorrowedBookList, '/books/borrowed/')
api.add_resource(AvailableBookList, '/books/available/')
api.add_resource(BorrowBook, '/books/<string(minlength=10, maxlength=13):isbn>/<int:_id>/loan')
api.add_resource(ReturnBook, '/books/<string(minlength=10, maxlength=13):isbn>/<int:_id>/return')

api.add_resource(CustomerList, '/customers/')
api.add_resource(Customer, '/customers/<int:_id>')
api.add_resource(CustomerListofBooks, '/customers/<int:_id>/books/', endpoint="api.borrowed_books")

api.add_resource(UserRegister, '/register')



if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
