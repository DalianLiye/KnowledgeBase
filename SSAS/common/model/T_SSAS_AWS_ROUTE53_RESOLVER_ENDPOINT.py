from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_ROUTE53_RESOLVER_ENDPOINT(Base):
    __tablename__ = 'SSAS_AWS_ROUTE53_RESOLVER_ENDPOINT'

    _account_id = Column("account_id", String, primary_key=True)
    _endpoint_type = Column("endpoint_type", String, primary_key=True)
    _endpoint_id = Column("endpoint_id", String, primary_key=True)
    _endpoint_name = Column("endpoint_name", String)
    _endpoint_status = Column("endpoint_status", String)
    _host_vpc = Column("host_vpc", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def endpoint_type(self):
        return self._endpoint_type

    @endpoint_type.setter
    def endpoint_type(self, value):
        self._endpoint_type = value

    @hybrid_property
    def endpoint_id(self):
        return self._endpoint_id

    @endpoint_id.setter
    def endpoint_id(self, value):
        self._endpoint_id = value

    @hybrid_property
    def endpoint_name(self):
        return self._endpoint_name

    @endpoint_name.setter
    def endpoint_name(self, value):
        self._endpoint_name = value

    @hybrid_property
    def endpoint_status(self):
        return self._endpoint_status

    @endpoint_status.setter
    def endpoint_status(self, value):
        self._endpoint_status = value

    @hybrid_property
    def host_vpc(self):
        return self._host_vpc

    @host_vpc.setter
    def host_vpc(self, value):
        self._host_vpc = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"endpoint_type='{self._endpoint_type}', " \
               f"endpoint_id='{self._endpoint_id}', " \
               f"endpoint_name='{self._endpoint_name}', " \
               f"endpoint_status='{self._endpoint_status}', " \
               f"host_vpc='{self._host_vpc}', " \
               f"create_time={self._create_time})>"