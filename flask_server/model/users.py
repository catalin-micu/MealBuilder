import json
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Integer, Column, String, SmallInteger, Boolean, func, DateTime, delete
from flask_server.model import BaseTable, logger


class UsersColumns:
    USER_ID = 'user_id'
    EMAIL = 'email'
    PASSWD = 'passwd'
    FULL_NAME = 'full_name'
    CARD_NB = 'card_nb'
    CARD_HOLDER_NAME = 'card_holder_name'
    CARD_EXPIRY = 'card_expiry'
    CVV = 'cvv'
    PREFERRED_ADDRESSES = 'preferred_addresses'
    ADMIN_PROFILE = 'admin_profile'
    CREATED_ON = 'created_on'
    LAST_LOGIN = 'last_login'
    PHONE_NUMBER = 'phone_number'


class Users(BaseTable):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    passwd = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    card_nb = Column(String)
    card_holder_name = Column(String)
    card_expiry = Column(String)
    cvv = Column(SmallInteger)
    preferred_addresses = Column(String)
    admin_profile = Column(Boolean, default=False)
    created_on = Column(DateTime, default=func.now())
    last_login = Column(DateTime, default=func.now(), onupdate=func.now())
    phone_number = Column(String, nullable=False, unique=True)

    def get_all_rows(self):
        rows = []
        for row in self.session.query(Users).all():
            rows.append(
                {
                    'user_id': row.user_id,
                    'email': row.email,
                    'passwd': row.passwd,
                    'name': row.full_name,
                    'created_on': row.created_on,
                    'last_login': row.last_login
                }
            )

        return rows

    def batch_upsert(self, path_to_file: str):
        """
        inserts or updates rows using json file as input: if franchise_id already exists, it will update the columns on
         that row (except restaurant_id, franchise_id, city) with the newly provided data
        :param path_to_file: str that represents the location of the input json
        """
        receipt = []
        abs_path = Path(path_to_file)   # file path object that matches os type
        with open(abs_path) as file:
            input_json = json.load(file)

        insert_stmt = insert(Users).values(input_json).returning(
            Users.full_name, Users.email, Users.preferred_addresses)
        columns_to_update = {col.name: col for col in insert_stmt.excluded
                             if col.name not in {UsersColumns.USER_ID,
                                                 UsersColumns.EMAIL, UsersColumns.PREFERRED_ADDRESSES}}
        upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=[Users.phone_number],
                                                        set_=columns_to_update)

        upserted_rows = self.session.execute(upsert_stmt)
        self.session.commit()

        for row in upserted_rows:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully upserted users: \n\t\t"
                    f"{', '.join([item.get(UsersColumns.FULL_NAME) for item in input_json])}\n"
                    f"from file: {path_to_file}")

        return receipt

    def delete_rows(self, rows_to_delete: list, identifier_type: str) -> []:
        """
        deletes rows based on an unique identifier (id / email / franchise_id, according to table definition)
        :param rows_to_delete: list of values that uniquely identify a row
        :param identifier_type: identifier for delete statement
        :return: list of dicts with info about deleted rows(name, franchise_id)
        """
        receipt = []
        if identifier_type not in {'id', 'email', 'phone_number'}:
            raise ValueError('Unknown identifier')

        delete_stmt = delete(Users)
        if identifier_type == 'id':
            delete_stmt = delete_stmt.where(Users.user_id.in_(rows_to_delete))
        elif identifier_type == 'email':
            delete_stmt = delete_stmt.where(Users.email.in_(rows_to_delete))
        else:
            delete_stmt = delete_stmt.where(Users.phone_number.in_(rows_to_delete))
        delete_stmt = delete_stmt.returning(Users.full_name, Users.email, Users.phone_number)

        deleted_rows = self.session.execute(delete_stmt).fetchall()
        self.session.commit()

        for row in deleted_rows:
            receipt.append(dict(row._mapping))

        return receipt