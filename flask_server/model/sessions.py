import json
from datetime import datetime
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Integer, Column, func, DateTime, delete, select, update, \
    ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_server.model import BaseTable, logger
from flask_server.model.users import Users, UsersColumns


class SessionsColumns:
    SESSION_ID = 'session_id'
    USER_ID = 'user_id'
    LAST_ACTION = 'last_action'


class Sessions(BaseTable):
    __tablename__ = 'sessions'

    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    last_action = Column(DateTime, default=func.now())

    users = relationship('Users', backref=backref("sessions", uselist=False))

    def create_session_from_email(self, email: str):    # no return type yet
        users_select_stmt = select(Users).where(Users.__table__.c[UsersColumns.EMAIL] == email)
        user_obj = self.session.execute(users_select_stmt).fetchone()

        if not user_obj:
            logger.critical(f"Cannot create session! Cannot find user with email '{email}'")
            raise StopIteration

        user_id = user_obj._data[0].user_id

        sessions_select_stmt = select(Sessions).where(Sessions.__table__.c[SessionsColumns.USER_ID] == user_id)
        if len(self.session.execute(sessions_select_stmt).fetchall()):
            logger.error(f"Session for user with email '{email}' already exists")
            raise StopIteration

        receipt = []

        insert_stmt = insert(Sessions).values(user_id=user_id)

        inserted_row = self.session.execute(insert_stmt)
        self.session.commit()

        for row in inserted_row:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully created session for user '{email}'")

        return receipt  # this shit is empty

    def update_last_action(self, user_id: int):
        update_stmt = update(Sessions).where(Sessions.user_id == user_id).\
            values(last_action=datetime.now()).returning(Sessions.user_id, Sessions.last_action)

        updated_row = self.session.execute(update_stmt)
        self.session.commit()
        last_action = [r[SessionsColumns.LAST_ACTION] for r in updated_row][0]

        logger.info(f"Updated last_action for user_id '{user_id}' to '{last_action}'")

    def delete_session(self, user_id: int):
        delete_stmt = delete(Sessions).where(Sessions.user_id == user_id)
        self.session.execute(delete_stmt)
        self.session.commit()
        logger.info(f"Successfully deleted session for user_id '{user_id}'")
