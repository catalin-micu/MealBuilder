from sqlalchemy.orm import relationship, backref
from flask_server.model import BaseTable, logger
import json
from pathlib import Path
from sqlalchemy import Column, Integer, String, ForeignKey, Date, select
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime


class ProgressColumns:
    RECORD_ID = 'record_id'
    EMAIL = 'email'
    WEIGHT = 'weight'
    CALORIES = 'calories'
    TIMESTAMP = 'timestamp'


PROGRESS_COLUMNS_LIST = [ProgressColumns.RECORD_ID, ProgressColumns.EMAIL, ProgressColumns.WEIGHT,
                         ProgressColumns.CALORIES, ProgressColumns.TIMESTAMP]


class Progress(BaseTable):
    __tablename__ = 'progress'

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, ForeignKey('users.email'), nullable=False, )
    weight = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)
    timestamp = Column(Date, default=datetime.today())

    restaurants = relationship('Users', backref=backref("progress", uselist=False))

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

        insert_stmt = insert(Progress).values(input_json).returning(Progress.email, Progress.calories, Progress.weight)
        columns_to_update = {col.name: col for col in insert_stmt.excluded
                             if col.name not in {ProgressColumns.RECORD_ID}}
        upsert_stmt = insert_stmt.on_conflict_do_update(index_elements=[Progress.record_id],
                                                        set_=columns_to_update)

        upserted_rows = self.session.execute(upsert_stmt)
        self.session.commit()

        for row in upserted_rows:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully upserted progress records: \n\t\t"
                    f"{', '.join([item.get(ProgressColumns.EMAIL) for item in input_json])}\n"
                    f"from file: {path}")

        return receipt

    def insert(self, progress_data: dict) -> list:
        receipt = []

        insert_stmt = insert(Progress).values(progress_data).returning(
            Progress.email, Progress.calories, Progress.weight)

        inserted_row = self.session.execute(insert_stmt)
        self.session.commit()

        for row in inserted_row:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully inserted progress record: \n\t\t{[progress_data.get(ProgressColumns.EMAIL)]}\n")

        return receipt

    def get_progress(self, email: str):
        select_stmt = select(Progress).where(Progress.__table__.c[ProgressColumns.EMAIL] == email)
        exec_result = self.session.execute(select_stmt)
        records = [super(Progress, Progress)._transform_row_into_dict(r, PROGRESS_COLUMNS_LIST)
                   for r in exec_result.fetchall()]

        return records
