from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, StoreList
from db import db

#JWT = json web token, we are going to use it as the user id, like sid in checkpoint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = "ek878"
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# change default endpoint from /auth to /login
app.config['JWT_AUTH_URL_RULE'] = '/login'
# change default token expiration frn 5 to 6 min
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
#jwt creates new endpoint /auth that gets username and password and return jwt token
jwt = JWT(app, authenticate, identity)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
 return jsonify({
     'access_token': access_token.decode('utf-8'),
     'user_id': identity.id
 })

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# only the file that we run get the name __main__, imports will not be with that name
if __name__ == "__main__":
    app.run(port=5000, debug=True)
