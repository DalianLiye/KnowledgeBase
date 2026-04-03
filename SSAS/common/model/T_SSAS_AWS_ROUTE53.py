from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_ROUTE53(Base):
    __tablename__ = 'SSAS_AWS_ROUTE53'

    _account_id = Column("account_id", String, primary_key=True)
    _host_zone_id = Column("host_zone_id", String, primary_key=True)
    _host_zone_name = Column("host_zone_name", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def host_zone_id(self):
        return self._host_zone_id

    @host_zone_id.setter
    def host_zone_id(self, value):
        self._host_zone_id = value

    @hybrid_property
    def host_zone_name(self):
        return self._host_zone_name

    @host_zone_name.setter
    def host_zone_name(self, value):
        self._host_zone_name = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"host_zone_id='{self._host_zone_id}', " \
               f"host_zone_name='{self._host_zone_name}', " \
               f"create_time={self._create_time})>"