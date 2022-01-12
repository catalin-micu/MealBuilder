import json
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Integer, Column, String, SmallInteger, Boolean, func, DateTime, delete, select, update
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


ACCEPTED_IDENTIFIER_TYPES = {UsersColumns.USER_ID, UsersColumns.EMAIL, UsersColumns.PHONE_NUMBER}


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
    last_login = Column(DateTime)
    phone_number = Column(String, nullable=False, unique=True)

    def batch_upsert_from_file(self, path_to_file: str) -> []:
        """
        ** don't think this will ever be used on production **
        inserts or updates rows using json file as input: if phone_number already exists, it will update a set of
         columns that make sense to be updated with the newly provided data
        :param path_to_file: str that represents the location of the input json
        :return : receipt list
        """
        receipt = []
        abs_path = Path(path_to_file)   # file path object that matches os type
        with open(abs_path) as file:
            input_json = json.load(file)

        insert_stmt = insert(Users).values(input_json).returning(
            Users.full_name, Users.email, Users.preferred_addresses)
        columns_to_update = {col.name: col for col in insert_stmt.excluded
                             if col.name not in {UsersColumns.USER_ID,
                                                 UsersColumns.EMAIL, UsersColumns.PREFERRED_ADDRESSES,
                                                 UsersColumns.CREATED_ON, UsersColumns.LAST_LOGIN,
                                                 UsersColumns.ADMIN_PROFILE}}
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
        deletes rows based on an unique identifier (user_id / email / phone_number, according to table definition)
        :param rows_to_delete: list of values that uniquely identify a row
        :param identifier_type: identifier for delete statement
        :return: list of dicts with info about deleted rows(name, email, phone_number)
        """
        receipt = []
        if identifier_type not in ACCEPTED_IDENTIFIER_TYPES:
            raise ValueError('Unknown identifier')

        delete_stmt = delete(Users)
        if identifier_type == UsersColumns.USER_ID:
            delete_stmt = delete_stmt.where(Users.user_id.in_(rows_to_delete))
        elif identifier_type == UsersColumns.EMAIL:
            delete_stmt = delete_stmt.where(Users.email.in_(rows_to_delete))
        else:
            delete_stmt = delete_stmt.where(Users.phone_number.in_(rows_to_delete))
        delete_stmt = delete_stmt.returning(Users.full_name, Users.email, Users.phone_number)

        deleted_rows = self.session.execute(delete_stmt).fetchall()
        self.session.commit()

        logger.info(f"Successfully deleted users with '{identifier_type}' identifier = '{rows_to_delete}'")

        for row in deleted_rows:
            receipt.append(dict(row._mapping))

        return receipt

    def insert_user(self, user_data: dict) -> list:
        """
        inserts a new user in the db if entry doesn't already exist
        :param user_data: dict with column name as keys and appropriate values
        :return: receipt list
        """
        if self.check_user_existence(identifier=user_data.get(UsersColumns.EMAIL), identifier_type=UsersColumns.EMAIL):
            logger.error(f"User with email '{user_data.get(UsersColumns.EMAIL)}' already exists")
            raise StopIteration

        receipt = []

        insert_stmt = insert(Users).values(user_data).returning(
            Users.full_name, Users.email, Users.preferred_addresses)

        inserted_row = self.session.execute(insert_stmt)
        self.session.commit()

        for row in inserted_row:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully inserted user: \n\t\t{[user_data.get(UsersColumns.FULL_NAME)]}\n")

        return receipt

    def check_user_existence(self, identifier: str, identifier_type: str) -> bool:
        """
        check if a user already exists in the db
        :param identifier: value of the unique identifier that is being used
        :param identifier_type: column name of the identifier
        :return: true if user is found else false
        """
        if identifier_type not in ACCEPTED_IDENTIFIER_TYPES:
            raise ValueError('Unknown identifier')

        select_stmt = select(Users).where(Users.__table__.c[identifier_type] == identifier)

        exec_result = self.session.execute(select_stmt)
        return bool(len(exec_result.fetchall()))

    def update_user(self, identifier: str, identifier_type: str, update_data: dict) -> []:
        if not self.check_user_existence(identifier=identifier, identifier_type=identifier_type):
            logger.error(f"User with '{identifier_type}' identifier = '{identifier}' does not exist")
            raise StopIteration

        receipt = []

        update_stmt = update(Users).where(Users.__table__.c[identifier_type] == identifier).values(update_data).\
            returning(Users.full_name, Users.email, Users.phone_number)

        updated_row = self.session.execute(update_stmt)
        self.session.commit()

        for row in updated_row:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully updated user with '{identifier_type}' identifier = '{identifier}'\n\t"
                    f"with data {update_data}")

        return receipt

    def check_login_credentials(self, email: str, passwd: str) -> bool:
        select_stmt = select(Users).where(Users.__table__.c[UsersColumns.EMAIL] == email).where(
                                          Users.__table__.c[UsersColumns.PASSWD] == passwd)
        selected_row = self.session.execute(select_stmt)
        rows = [r for r in selected_row]
        return bool(len(rows))

    def get_user_id_from_email(self, email: str) -> int:
        select_stmt = select(Users).where(Users.email == email)
        res = self.session.execute(select_stmt)
        user = [r for r in res.fetchall()][0]

        return user._data[0].user_id
