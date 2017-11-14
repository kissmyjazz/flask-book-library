from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.customer import CustomerModel

class Customer(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name',
        type=str,
        required=False,
        help="Name of the customer.")

    @jwt_required()
    def get(self, _id):
        customer = CustomerModel.get_by_id(_id)
        if customer:
            return customer.json
        return {'message': 'Customer not found'}, 404

    @jwt_required()
    def post(self, _id):
        if CustomerModel.get_by_id(_id):
            return {'message': "A customer with an id '{}' already exists.".format(_id)}, 400

        data = Customer.parser.parse_args()

        customer = CustomerModel(_id=_id, **data)

        try:
            customer.save_to_db()
        except:
            return {"message": "An error occurred inserting the customer."}, 500

        return customer.json, 201

    @jwt_required()
    def delete(self, _id):
        customer = CustomerModel.get_by_id(_id)
        if customer:
            customer.delete_from_db()

        return {'message': 'Customer deleted'}

    @jwt_required()  
    def put(self, _id):
        data = Customer.parser.parse_args()

        customer = CustomerModel.get_by_id(_id)

        if customer is None:
            customer = CustomerModel(_id=_id, **data)
        else:
            if 'name' in data:
                customer.name = data['name']

        customer.save_to_db()

        return customer.json()


class CustomerList(Resource):
    @jwt_required()
    def get(self):
        return {'Customers': [x.json for x in CustomerModel.query.all()]}


class CustomerListofBooks(Resource):
    @jwt_required()
    def get(self, _id):
        customer = CustomerModel.get_by_id(_id)
        if customer:
            return customer.json_books
        return {'message': 'Customer not found'}, 404
