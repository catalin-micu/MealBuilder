from sqlalchemy import Integer, Column, String, SmallInteger
from flask_server.model import BaseTable


class UsersColumns:
    USER_ID = 'user_id'
    EMAIL = 'email'
    PASSWD = 'passwd'
    FULL_NAME = 'full_name'
    CARD_NB = 'card_nb'
    CARD_HOLDER_NAME = 'card_holder_name'
    CARD_EXPIRY = 'card_expiry'
    CVV = 'cvv'
    PREFERRED_ADDRESS = 'preferred_address'


class Users(BaseTable):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    passwd = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    card_nb = Column(String)
    card_holder_name = Column(String)
    card_expiry = Column(String)
    cvv = Column(SmallInteger)
    preferred_address = Column(String)

    def get_all_rows(self):
        rows = []
        for row in self.session.query(Users).all():
            rows.append(
                {
                    'user_id': row.user_id,
                    'email': row.email,
                    'passwd': row.passwd,
                    'name': row.full_name
                }
            )

        return rows
