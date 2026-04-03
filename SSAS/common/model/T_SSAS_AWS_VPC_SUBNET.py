from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_VPC_SUBNET(Base):
    __tablename__ = 'SSAS_AWS_VPC_SUBNET'

    _account_id = Column("account_id", String, primary_key=True)
    _vpc_id = Column("vpc_id", String, primary_key=True)
    _subnet_id = Column("subnet_id", String, primary_key=True)
    _subnet_name = Column("subnet_name", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def vpc_id(self):
        return self._vpc_id

    @vpc_id.setter
    def vpc_id(self, value):
        self._vpc_id = value

    @hybrid_property
    def subnet_id(self):
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, value):
        self._subnet_id = value

    @hybrid_property
    def subnet_name(self):
        return self._subnet_name

    @subnet_name.setter
    def subnet_name(self, value):
        self._subnet_name = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id={self._account_id}, " \
               f"vpc_id={self._vpc_id}, " \
               f"subnet_id={self._subnet_id}, " \
               f"subnet_name={self._subnet_name}, " \
               f"create_time={self._create_time})>"