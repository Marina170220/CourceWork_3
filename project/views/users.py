from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.users_service import UsersService
from project.setup_db import db
from project.tools.security import auth_required, admin_required, auth_check, get_id_from_token

users_ns = Namespace("user")


@users_ns.route('/')
class UserView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def get(self):
        """Get user by id"""
        user_id = get_id_from_token()
        try:
            return UsersService(db.session).get_user_by_id(user_id)
        except ItemNotFound:
            abort(404)

    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def patch(self):
        """Update user's data"""
        req_json = request.json
        if not req_json:
            abort(400)
        uid = get_id_from_token()
        try:
            return UsersService(db.session).update(req_json, uid)
        except ItemNotFound:
            abort(404)


@users_ns.route('/password')
class UserPatchView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def put(self):
        """Update user's password"""
        req_json = request.json
        if not req_json:
            abort(400)
        if not req_json.get('password_1') or not req_json.get('password_2'):
            abort(400)
        uid = get_id_from_token()
        try:
            return UsersService(db.session).update_user_pass(req_json, uid)
        except ItemNotFound:
            abort(404)

#
# @users_ns.route('/all')
# class UsersView(Resource):
#     @admin_required
#     @users_ns.response(200, "OK")
#     def get(self):
#         """Get all users (available only to admins)"""
#         page = request.args.get('page')
#         if page:
#             return UsersService(db.session).get_limit_users(page)
#
#         return UsersService(db.session).get_all_users()


