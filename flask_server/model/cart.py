from sqlalchemy.orm import relationship, backref
from flask_server.model import BaseTable, logger
import json
from pathlib import Path
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import insert


class Cart(BaseTable):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)

    # relationship, maybe change for products?
