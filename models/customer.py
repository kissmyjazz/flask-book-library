from db import db
from models.book import BookModel
from flask import url_for


class CustomerModel(db.Model):
    __tablename__ = 'customers'
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), index=True, nullable=False)
    books = db.relationship('BookModel', backref='customer', lazy='dynamic')

    def get_url(self):
        return url_for('api.borrowed_books', _id=self._id, _external=True)

    @property
    def json(self):
        return {
            'name': self.name
        }

    @property
    def json_books(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'number of loaned books': BookModel.query.filter_by(customer_id = self._id).filter(BookModel.loaned == True).count(),
            'loaned books': [book._base_json for book in BookModel.query.filter_by(customer_id = self._id).all()]

        }

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
