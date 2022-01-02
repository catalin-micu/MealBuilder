from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


con_url = 'postgresql://postgres:password@localhost:5432/meal_builder'
engine = create_engine(con_url)
Session = sessionmaker(bind=engine)


Base = declarative_base()


class BaseTable(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = Session()

    def get_execution_receipt(self, input_rows: list) -> tuple:
        """
        generic method that computes db transaction receipt for upsert and delete (what db transactions succeeded and
        what did not)
        :param input_rows: list of dicts that contain appropriate data (respects table definitions) in order to
         complete transaction execution
        :return: tuple of 2 lists for succeeded transactions and failed transactions
        """
        succeeded, failed = ([], [])

        return succeeded, failed

    def was_upserted(self, rows_to_upsert: list) -> set:
        """
        check if input rows have been stored to the db (new rows / updated existing rows)
        :param rows_to_upsert: list of dicts that contain items according to table definitions
        :return: set of successfully upserted rows
        """
        upserted_rows = set()

        return upserted_rows

    def was_deleted(self, rows_to_delete: list) -> set:
        """
        check if input rows have been deleted
        :param rows_to_delete: list of dicts that contain enough data (according to table definitions) to identify
         the rows that need to be deleted
        :return: set of successfully deleted rows
        """
        deleted_rows = set()

        return deleted_rows
