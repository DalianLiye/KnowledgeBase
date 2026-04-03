from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_DYNAMODB(Base):
    __tablename__ = 'SSAS_AWS_DYNAMODB'

    _account_id = Column("account_id", String, primary_key=True)
    _table_name = Column("table_name", String, primary_key=True)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        self._table_name = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"table_name='{self._table_name}', " \
               f"create_time={self._create_time})>"