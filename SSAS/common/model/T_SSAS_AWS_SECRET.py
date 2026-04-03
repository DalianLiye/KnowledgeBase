from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_SECRET(Base):
    __tablename__ = 'SSAS_AWS_SECRET'

    _account_id = Column("account_id", String, primary_key=True)
    _secret_name = Column("secret_name", String, primary_key=True)
    _secret_value = Column("secret_value", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def secret_name(self):
        return self._secret_name

    @secret_name.setter
    def secret_name(self, value):
        self._secret_name = value

    @hybrid_property
    def secret_value(self):
        return self._secret_value

    @secret_value.setter
    def secret_value(self, value):
        self._secret_value = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"secret_name='{self._secret_name}', " \
               f"secret_value='{self._secret_value}', " \
               f"create_time={self._create_time})>"