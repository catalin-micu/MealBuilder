from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import insert

from flask_server.model import Base, Session


class Restaurants(Base):
    __tablename__ = 'restaurants'

    restaurant_id = Column(Integer, primary_key=True)
    restaurant_name = Column(String, nullable=False)
    franchise_id = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    passwd = Column(String, nullable=False)
    city = Column(String, nullable=False)
    provides_custom_meals = Column(Boolean, default=False)
    provides_scheduled_delivery = Column(Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = Session()

    def upsert_row(self, rows: list):
        """
        inserts or updates rows: if franchise_id already exists, it will update the columns on that row
         (except restaurant_id, franchise_id, city) with the newly provided data
        :param rows: list of dicts; keys of dict items = column names
        """
        insert_stmt = insert(Restaurants).values(rows)
        columns_to_update = {col.name: col for col in insert_stmt.excluded
                             if col.name not in {'restaurant_id', 'franchise_id', 'city'}}
        upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=[Restaurants.franchise_id],
                                                        set_=columns_to_update)
        self.session.execute(upsert_stmt)
        self.session.commit()
