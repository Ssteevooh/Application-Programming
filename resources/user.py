from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from flask import request
from http import HTTPStatus
from flask_restful import Resource
from models.user import User
from utils import hash_password
from schemas.user import UserSchema
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.instruction import Instruction
from schemas.instruction import InstructionSchema

user_schema = UserSchema()
user_public_scheme = UserSchema(exclude=('email',))
instruction_list_schema = InstructionSchema(many=True)

class UserInstructionListResource(Resource):

    @jwt_optional
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, username, visibility):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'

            instructions = Instruction.get_all_by_user(user_id=user.id, visibility=visibility)
            return instruction_list_schema.dump(instructions).data, HTTPStatus.OK


class UserListResource(Resource):

    def post(self):

        json_data = request.get_json()
        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': "Validation Errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get("username")):
            return {"message": "Username is already in use"}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get("email")):
            return {"message": "Email is already in use"}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        return user_schema.dump(user).data, HTTPStatus.CREATED

class UserResource(Resource):

    @jwt_optional
    def get(self, username):

        user = User.get_by_username(username=username)

        if user is None:

            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user).data

        else:
            data = user_public_scheme.dump(user).data
        return data, HTTPStatus.OK

class MeResource(Resource):

    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        return user_schema.dump(user).data, HTTPStatus.OK
