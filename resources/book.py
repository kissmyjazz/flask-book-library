from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.book import BookModel
from models.customer import CustomerModel

class Book(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('title',
        type=str,
        required=False,
        help="Title of the book.")

    parser.add_argument('author',
        type=str,
        required=False,
        help="Author of the book."
    )

    parser.add_argument('year',
        type=int,
        required=False,
        help="Year when the book was published."
    )

    parser.add_argument('publisher',
        type=str,
        required=False,
        help="Publisher of the book."
    )

    parser.add_argument('loaned',
        type=bool,
        required=False,
        help="Shows if book is available."
    )

    parser.add_argument('customer_id',
        type=int,
        required=False,
        help="Customer who has loaned the book."
    )


    def get(self, isbn):
        book = BookModel.find_by_isbn(str(isbn))
        if book:
            return book.json
        return {'message': 'book not found'}, 404

    @jwt_required()
    def post(self, isbn):
        if BookModel.find_by_isbn(str(isbn)):
            return {'message': "A book with isbn '{}' already exists.".format(str(isbn))}, 400

        data = Book.parser.parse_args()

        book = BookModel(isbn=str(isbn), **data)

        try:
            book.save_to_db()
        except:
            return {"message": "An error occurred inserting the book."}, 500

        return book.json, 201

    @jwt_required()
    def delete(self, isbn):
        book = BookModel.find_by_isbn(str(isbn))
        if book:
            book.delete_from_db()

        return {'message': 'book deleted'}

    @jwt_required()
    def put(self, isbn):
        data = Book.parser.parse_args()

        book = BookModel.find_by_isbn(str(isbn))

        if book is None:
            book = BookModel(isbn=str(isbn), **data)
        else:
            if 'title' in data:
                book.title = data['title']
            if 'author' in data:
                book.author = data['author']
            if 'year' in data:
                book.year = data['year']
            if 'publisher' in data:
                book.publisher = data['publisher']
            if 'loaned' in data:
                book.loaned = data['loaned']
            if 'customer_id' in data:
                book.customer_id = data['customer_id']

        book.save_to_db()

        return book.json


class BookList(Resource):
    def get(self):
        return {'books': [x.json for x in BookModel.query.all()]}


class BorrowedBookList(Resource):
    def get(self):
        return {'loaned books': [x._base_json for x in BookModel.query.filter(BookModel.loaned==True).all()]}


class AvailableBookList(Resource):
    def get(self):
        return {'available books': [x._base_json for x in BookModel.query.filter(BookModel.loaned==False).all()]}


class BorrowBook(Resource):
    @jwt_required()
    def post(self, isbn, _id):
        book = BookModel.find_by_isbn(str(isbn))
        if book is None:
            return {'message': 'book not found'}, 404
        if bool(book.loaned):
            return {'message': 'the requested book has been already borrowed'}, 405

        customer = CustomerModel.get_by_id(_id)
        if customer is None:
            return {'message': 'customer not found'}, 404  
        book.loaned = True
        book.customer_id = _id
        customer.books.append(book)
        book.save_to_db()
        customer.save_to_db()
        return {'message': 'the book has been borrowed successfully'}, 201


class ReturnBook(Resource):
    @jwt_required()
    def post(self, isbn, _id):
        book = BookModel.find_by_isbn(str(isbn))
        if book is None:
            return {'message': 'book not found'}, 404
        if bool(book.loaned) == False:
            return {'message': 'the requested book is not borrowed'}, 405

        customer = CustomerModel.get_by_id(_id)
        if customer is None:
            return {'message': 'customer not found'}, 404  
        book.loaned = False
        book.customer_id = None
        customer.books.remove(book)
        book.save_to_db()
        customer.save_to_db()
        return {'message': 'the book has been returned successfully'}, 201
