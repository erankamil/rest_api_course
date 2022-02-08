from flask_restful import Resource, reqparse
from models.user import UserModel

# create resource endpoint to register users
class UserRegister(Resource):
    # use the parser to parse the request
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be empty")
    parser.add_argument('password', type=str, required=True, help="This field cannot be empty")

    def post(self):
        data = UserRegister.parser.parse_args()

        # we want to make sure there is not duplicate users
        if UserModel.find_by_username(data['username']):
            return {"message": "this username already exist in the system"}, 400

        try:
            UserModel.save_to_db(UserModel(**data))
        except:
            return {"message": "An error occurred when saving user to db"}

        return {"message": "User created successfully"}, 201

