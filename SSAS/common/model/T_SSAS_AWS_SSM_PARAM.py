from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_SSM_PARAM(Base):
    __tablename__ = 'SSAS_AWS_SSM_PARAM'

    _account_id = Column("account_id", String, primary_key=True)
    _param_name = Column("param_name", String, primary_key=True)
    _param_tier = Column("param_tier", String)
    _param_type = Column("param_type", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def param_name(self):
        return self._param_name

    @param_name.setter
    def param_name(self, value):
        self._param_name = value

    @hybrid_property
    def param_tier(self):
        return self._param_tier

    @param_tier.setter
    def param_tier(self, value):
        self._param_tier = value

    @hybrid_property
    def param_type(self):
        return self._param_type

    @param_type.setter
    def param_type(self, value):
        self._param_type = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"param_name='{self._param_name}', " \
               f"param_tier='{self._param_tier}', " \
               f"param_type='{self._param_type}', " \
               f"create_time={self._create_time})>"