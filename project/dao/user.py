from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_one_by_id(self, pk):
        """
        Получаем пользователя из БД по его id.
        Param pk: id пользователя.
        Return: пользователь из БД если найден, либо None.
        """
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        """
        Получаем пользователя из БД по его имейлу.
        Param email: email пользователя (он же логин).
        Return: пользователь из БД если найден, либо None.
        """
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        """
        Получаем всех пользователей из БД.
        Return: список всех пользователей из БД.
        """
        return self._db_session.query(User).all()

    def get_by_limit(self, limit, offset):
        """
        Получаем всех пользователей из БД с учётом ограничений по выдаче.
        Param limit: количество пользователей на одной странице выдачи.
        Param offset: количество пользователей, которое нужно пропустить перед выводом.
        Return: список всех пользователей из БД с учётом лимита и отступа.
        """
        return self._db_session.query(User).limit(limit).offset(offset).all()

    def create(self, user_data):
        """
        Создаём нового пользователя.
        Param data: данные, введённые пользователем при регистрации.
        Return: новый пользователь.
        """
        user = User(**user_data)
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def update(self, user):
        """
        Обновляем данные пользователя.
        Param user: пользователь, данные которого необходимо обновить.
        Return: пользователь с обновлёнными данными.
        """
        self._db_session.add(user)
        self._db_session.commit()
        return user
