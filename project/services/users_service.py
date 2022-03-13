from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.config import BaseConfig
from project.tools.security import generate_password_hash, compare_passwords


class UsersService(BaseService):
    def get_user_by_id(self, pk):
        user = UserDAO(self._db_session).get_one_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def get_user_by_email(self, email):
        user = UserDAO(self._db_session).get_by_email(email)
        return UserSchema().dump(user)

    def get_limit_users(self, page):
        limit = BaseConfig.ITEMS_PER_PAGE
        offset = (page - 1) * limit
        users = UserDAO(self._db_session).get_by_limit(limit=limit, offset=offset)
        return UserSchema(many=True).dump(users)

    def create(self, user_data):
        user_password = user_data.get('password')
        if user_password:
            user_data['password'] = generate_password_hash(user_password)
        user = UserDAO(self._db_session).create(user_data)
        return UserSchema().dump(user)

    def update(self, user_data):
        user = self.get_user_by_id(user_data.get('id'))
        if user:
            if user_data.get('name'):
                user.name = user_data.get('name')
            if user_data.get('surname'):
                user.surname = user_data.get('surname')
            if user_data.get('favorite_genre'):
                user.favorite_genre = user_data.get('favorite_genre')

            updated_user = UserDAO(self._db_session).update(user)
            return UserSchema().dump(updated_user)
        return None

    def update_user_pass(self, user_data):
        user_password_old = user_data.get('password_1')
        user_password_new = user_data.get('password_2')
        user = self.get_user_by_id(user_data.get('id'))
        if user:
            if compare_passwords(user.password, user_password_old):
                user['password'] = generate_password_hash(user_password_new)
            updated_user = UserDAO(self._db_session).update(user)
            return UserSchema().dump(updated_user)
        return None
