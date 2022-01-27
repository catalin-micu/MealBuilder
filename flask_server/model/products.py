from sqlalchemy.orm import relationship, backref
from flask_server.model import BaseTable, logger
import json
from pathlib import Path
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import insert

from flask_server.model.restaurants import Restaurants


class ProductsColumns:
    PRODUCT_ID = 'product_id'
    NAME = 'name'
    RESTAURANT_ID = 'restaurant_id'
    FOOD_TYPE = 'food_type'
    CALORIES = 'calories'
    PROTEIN = 'protein'
    CARBS = 'carbs'
    FAT = 'fat'
    COOKING_METHOD = 'cooking_method'
    COOKING_DETAILS = 'cooking_details'
    IDENTIFIER = 'identifier'
    PRICE = 'price'
    CURRENCY = 'currency'


PRODUCTS_COLUMNS_LIST = [ProductsColumns.PRODUCT_ID, ProductsColumns.NAME, ProductsColumns.RESTAURANT_ID,
                         ProductsColumns.FOOD_TYPE, ProductsColumns.CALORIES, ProductsColumns.PROTEIN,
                         ProductsColumns.CARBS, ProductsColumns.FAT, ProductsColumns.COOKING_METHOD,
                         ProductsColumns.COOKING_DETAILS, ProductsColumns.IDENTIFIER, ProductsColumns.PRICE, ProductsColumns.CURRENCY]


class Products(BaseTable):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'), nullable=False)
    food_type = Column(String, nullable=False)  # (protein, carb, fat, meal)
    calories = Column(Integer, nullable=False)
    protein = Column(Integer, nullable=False)
    carbs = Column(Integer, nullable=False)
    fat = Column(Integer, nullable=False)
    cooking_method = Column(String)
    cooking_details = Column(String, nullable=False)
    identifier = Column(String, unique=True)    # f'{name}/{restaurant_id}'
    price = Column(Integer, nullable=False)
    currency = Column(String, default="RON")

    restaurants = relationship('Restaurants', backref=backref("products", uselist=False))

    def upsert_products_from_file(self, path: str) -> []:
        """
        inserts or updates rows using json file as input: if identifier already exists, it will update the columns on
         that row (except product_id, name, restaurant_id, identifier) with the newly provided data
        :param path: path to json input file
        :return: receipt list with updated data
        """
        receipt = []
        abs_path = Path(path)  # file path object that matches os type
        with open(abs_path) as file:
            input_json = json.load(file)

        for item in input_json:
            item['identifier'] = f"{item['name']}/{item['restaurant_id']}"

        insert_stmt = insert(Products).values(input_json).returning(Products.name, Products.food_type)
        columns_to_update = {col.name: col for col in insert_stmt.excluded
                             if col.name not in {ProductsColumns.PRODUCT_ID, ProductsColumns.NAME,
                                                 ProductsColumns.RESTAURANT_ID, ProductsColumns.IDENTIFIER}}
        upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=[Products.identifier],
                                                        set_=columns_to_update)

        upserted_rows = self.session.execute(upsert_stmt)
        self.session.commit()

        for row in upserted_rows:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully upserted products: \n\t\t"
                    f"{', '.join([item.get(ProductsColumns.NAME) for item in input_json])}\n"
                    f"from file: {path}")

        return receipt

    def get_restaurant_products(self, restaurant: str, food_type: str) -> []:
        products = []
        q = self.session.query(Products).filter(Products.food_type == food_type).join(Products.restaurants).\
            filter(Restaurants.restaurant_name == restaurant).all()
        for o in q:
            products.append(super(Products, Products)._transform_table_obj_into_dict(o, PRODUCTS_COLUMNS_LIST))

        return products
