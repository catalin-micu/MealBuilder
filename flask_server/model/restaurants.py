import json
from pathlib import Path
from sqlalchemy import Column, Integer, String, Boolean, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Row

from flask_server.model import BaseTable, logger


class RestaurantsColumns:
    RESTAURANT_ID = 'restaurant_id'
    RESTAURANT_NAME = 'restaurant_name'
    FRANCHISE_ID = 'franchise_id'
    EMAIL = 'email'
    PASSWD = 'passwd'
    CITY = 'city'
    PROVIDES_CUSTOM_MEALS = 'provides_custom_meals'
    PROVIDES_CUSTOM_DELIVERY = 'provides_scheduled_delivery'


RESTAURANTS_COLUMNS_LIST = [RestaurantsColumns.RESTAURANT_ID, RestaurantsColumns.RESTAURANT_NAME,
                            RestaurantsColumns.FRANCHISE_ID, RestaurantsColumns.EMAIL, RestaurantsColumns.PASSWD,
                            RestaurantsColumns.CITY, RestaurantsColumns.PROVIDES_CUSTOM_MEALS,
                            RestaurantsColumns.PROVIDES_CUSTOM_DELIVERY]


class Restaurants(BaseTable):
    __tablename__ = 'restaurants'

    restaurant_id = Column(Integer, primary_key=True)
    restaurant_name = Column(String, nullable=False)
    franchise_id = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    passwd = Column(String, nullable=False)
    city = Column(String, nullable=False)
    provides_custom_meals = Column(Boolean, default=False)
    provides_scheduled_delivery = Column(Boolean, default=False)

    def upsert_row(self, rows: list):
        """
        inserts or updates rows: if franchise_id already exists, it will update the columns on that row
         (except restaurant_id, franchise_id, city) with the newly provided data
        implemented for testing mainly, can be deleted later
        :param rows: list of dicts; keys of dict items = column names
        """
        receipt = []
        insert_stmt = insert(Restaurants).values(rows).returning(
            Restaurants.restaurant_name, Restaurants.franchise_id)
        columns_to_update = {col.name: col for col in insert_stmt.excluded
                             if col.name not in {RestaurantsColumns.RESTAURANT_ID,
                                                 RestaurantsColumns.FRANCHISE_ID, RestaurantsColumns.CITY}}
        upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=[Restaurants.franchise_id],
                                                        set_=columns_to_update)

        upserted_rows = self.session.execute(upsert_stmt)
        self.session.commit()

        for row in upserted_rows:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully upserted following restaurants:\n\t\t"
                    f"{', '.join([item.get(RestaurantsColumns.RESTAURANT_NAME) for item in rows])}")

        return receipt

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

        insert_stmt = insert(Restaurants).values(input_json).returning(
            Restaurants.restaurant_name, Restaurants.franchise_id)
        columns_to_update = {col.name: col for col in insert_stmt.excluded
                             if col.name not in {RestaurantsColumns.RESTAURANT_ID,
                                                 RestaurantsColumns.FRANCHISE_ID, RestaurantsColumns.CITY}}
        upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=[Restaurants.franchise_id],
                                                        set_=columns_to_update)

        upserted_rows = self.session.execute(upsert_stmt)
        self.session.commit()

        for row in upserted_rows:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully upserted restaurants: \n\t\t"
                    f"{', '.join([item.get(RestaurantsColumns.RESTAURANT_NAME) for item in input_json])}\n"
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
        if identifier_type not in {'id', 'email', 'franchise_id'}:
            raise ValueError('Unknown identifier')

        delete_stmt = delete(Restaurants)
        if identifier_type == 'id':
            delete_stmt = delete_stmt.where(Restaurants.restaurant_id.in_(rows_to_delete))
        elif identifier_type == 'email':
            delete_stmt = delete_stmt.where(Restaurants.email.in_(rows_to_delete))
        else:
            delete_stmt = delete_stmt.where(Restaurants.franchise_id.in_(rows_to_delete))
        delete_stmt = delete_stmt.returning(Restaurants.restaurant_name, Restaurants.franchise_id)

        deleted_rows = self.session.execute(delete_stmt).fetchall()
        self.session.commit()

        for row in deleted_rows:
            receipt.append(dict(row._mapping))

        return receipt

    def get_restaurants_in_given_city(self, city: str) -> []:
        """
        gets all the restaurants in a given city
        :param city: city to query after
        :return: list of dicts with data (keys mapped according to table column names)
        """
        rests_list = []
        select_stmt = select(Restaurants).where(Restaurants.city == city)
        rests = self.session.execute(select_stmt).fetchall()
        for r in rests:
            rests_list.append(super(Restaurants, Restaurants)._transform_row_into_dict(r, RESTAURANTS_COLUMNS_LIST))

        return rests_list

    def search_restaurants_by_name(self, input_name: str) -> []:
        """
        gets restaurant details based on name
        :param input_name: full name of the restaurant
        :return: list of dicts with data (keys mapped according to table column names)
        """
        rests_list = []
        select_stmt = select(Restaurants).where(Restaurants.restaurant_name.like(f'{input_name}'))
        res = self.session.execute(select_stmt).fetchall()
        for r in res:
            rests_list.append(super(Restaurants, Restaurants)._transform_row_into_dict(r, RESTAURANTS_COLUMNS_LIST))

        return rests_list
