from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_ACCOUNT(Base):
    __tablename__ = 'SSAS_AWS_ACCOUNT'

    _env = Column("env", String, primary_key=True)
    _account_id= Column("account_id", String, primary_key=True)
    _account_name = Column("account_name", String)
    _create_time = Column("create_time",TIMESTAMP)

    @hybrid_property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        self._env = value

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, value):
        self.__account_name = value

    @hybrid_property
    def create_time(self):
        return self.__create_time

    @create_time.setter
    def create_time(self, value):
        self.__create_time = value

    def __repr__(self):
        return f"<MyTable(env={self._env}, " \
               f"account_id={self._account_id}, " \
               f"account_name={self._account_name}, " \
               f"create_time={self._create_time})>"