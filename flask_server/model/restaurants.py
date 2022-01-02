import json
from pathlib import Path
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import insert
from flask_server.model import Base, BaseTable


class RestaurantsColumns:
    RESTAURANT_ID = 'restaurant_id'
    RESTAURANT_NAME = 'restaurant_name'
    FRANCHISE_ID = 'franchise_id'
    EMAIL = 'email'
    PASSWD = 'passwd'
    CITY = 'city'
    PROVIDES_CUSTOM_MEALS = 'provides_custom_meals'
    PROVIDES_CUSTOM_DELIVERY = 'provides_scheduled_delivery'


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


    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def upsert_row(self, rows: list):
        """
        inserts or updates rows: if franchise_id already exists, it will update the columns on that row
         (except restaurant_id, franchise_id, city) with the newly provided data
        implemented for testing mainly, can be deleted later
        :param rows: list of dicts; keys of dict items = column names
        """
        insert_stmt = insert(Restaurants).values(rows)
        columns_to_update = {col.name: col for col in insert_stmt.excluded
                             if col.name not in {RestaurantsColumns.RESTAURANT_ID,
                                                 RestaurantsColumns.FRANCHISE_ID, RestaurantsColumns.CITY}}
        upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=[Restaurants.franchise_id],
                                                        set_=columns_to_update)
        self.session.execute(upsert_stmt)
        self.session.commit()

    def batch_upsert(self, path_to_file: str):
        """
        inserts or updates rows using json file as input: if franchise_id already exists, it will update the columns on
         that row (except restaurant_id, franchise_id, city) with the newly provided data
        :param path_to_file: str that represents the location of the input json
        """
        abs_path = Path(path_to_file)   # file path object that matches os type
        input_json = json.load(open(abs_path))

        insert_stmt = insert(Restaurants).values(input_json)
        columns_to_update = {col.name: col for col in insert_stmt.excluded
                             if col.name not in {RestaurantsColumns.RESTAURANT_ID,
                                                 RestaurantsColumns.FRANCHISE_ID, RestaurantsColumns.CITY}}
        upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=[Restaurants.franchise_id],
                                                        set_=columns_to_update)

        self.session.execute(upsert_stmt)
        self.session.commit()
