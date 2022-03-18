from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.config import BaseConfig
from project.tools.security import generate_password_hash, compare_passwords


class UsersService(BaseService):
    def get_user_by_id(self, pk):
        """
        Получаем пользователя по его id.
        Param pk: id пользователя.
        """
        user = UserDAO(self._db_session).get_one_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        """
        Получаем всех пользователей.
        """
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def get_user_by_email(self, email):
        """
        Получаем пользователя из БД по его имейлу.
        Param email: email пользователя (он же логин).
        """
        user = UserDAO(self._db_session).get_by_email(email)
        return UserSchema().dump(user)

    def get_limit_users(self, page):
        """
        Получаем всех пользователей из БД с учётом ограничений по выдаче.
        Param page: номер страницы выдачи.
        """
        limit = BaseConfig.ITEMS_PER_PAGE
        offset = (int(page) - 1) * limit
        users = UserDAO(self._db_session).get_by_limit(limit=limit, offset=offset)
        return UserSchema(many=True).dump(users)

    def create(self, user_data):
        """
        Создаём нового пользователя.
        Param data: данные, введённые пользователем при регистрации.
        """
        user_password = user_data.get('password')
        if user_password:
            user_data['password'] = generate_password_hash(user_password)
            user = UserDAO(self._db_session).create(user_data)
            return UserSchema().dump(user)
        return None

    def update(self, user_data, uid):
        """
        Обновляем данные пользователя.
        Param user_data: данные пользователя, которые необходимо обновить.
        Param uid: id пользователя, чьи данные обновляем (получаем из токена).
        """
        user = UserDAO(self._db_session).get_one_by_id(uid)
        if user_data.get('name'):
            user.name = user_data.get('name')
        if user_data.get('surname'):
            user.surname = user_data.get('surname')
        if user_data.get('favorite_genre_id'):
            user.favorite_genre_id = user_data.get('favorite_genre_id')

        updated_user = UserDAO(self._db_session).update(user)
        return UserSchema().dump(updated_user)

    def update_user_pass(self, user_data, uid):
        """
        Обновляем пароль пользователя, для этого нужно отправить два пароля password_1 и password_2.
        Перед тем, как установить новый пароль, проверяем, совпадает ли старый с паролем, хранящимся в БД.
        Param user_data: данные со старым и новым паролем, введённые пользователем.
        Param uid: id пользователя, чьи пароли обновляем (получаем из токена).

        """
        user_password_old = user_data.get('password_1')
        user_password_new = user_data.get('password_2')
        user = UserDAO(self._db_session).get_one_by_id(uid)
        if compare_passwords(user.password, user_password_old):
            user.password = generate_password_hash(user_password_new)
            updated_user = UserDAO(self._db_session).update(user)
            return UserSchema().dump(updated_user)
        return None
