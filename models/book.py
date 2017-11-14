from db import db
from flask import url_for


class BookModel(db.Model):
    __tablename__ = 'books'
    _id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    title = db.Column(db.Unicode(300), nullable=True, index=True)
    author = db.Column(db.Unicode(100), nullable=True, index=True)
    year = db.Column(db.Integer(), nullable=True)
    publisher = db.Column(db.Unicode(200), nullable=True)
    loaned = db.Column(db.Boolean(), default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers._id'))

    @property
    def _base_json(self):
        return {
            'self_url': self.get_url(),
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'publisher': self.publisher
            }


    def get_url(self):
        return url_for('api.book_details', isbn=self.isbn, _external=True)

    @property
    def json(self):
        json = self._base_json
        if bool(self.loaned):
            json['loan status'] = 'loaned out'
        else:
            json['loan status'] = 'available'
        return json

    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(int(id))

    @classmethod
    def is_loaned(cls, isbn):
        book = cls.query.filter_by(isbn=isbn).first().loaned


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()