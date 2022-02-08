from models.user import UserModel
from hmac import compare_digest
from hashlib import sha512

def authenticate(username, password):
    # use default value with get method to not get exception
    user = UserModel.find_by_username(username)
    if user and compare_digest(user.hashed_password,
                               sha512(password.encode('utf-8') + user.salt).digest()):
        return user

# the payload is the contect of the request, in case we decorate our endpoints with @jwt_required()
def identity(payload):
    # extract the uid from the payload
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
