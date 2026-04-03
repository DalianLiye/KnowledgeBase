from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_ACM_CERTIFICATE(Base):
    __tablename__ = 'SSAS_AWS_ACM_CERTIFICATE'

    _account_id = Column("account_id", String, primary_key=True)
    _certificate_id = Column("certificate_id", String, primary_key=True)
    _domain_name = Column("domain_name", String)
    _certificate_type = Column("certificate_type", String)
    _certificate_status = Column("certificate_status", String)
    _is_in_use = Column("is_in_use", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def certificate_id(self):
        return self._certificate_id

    @certificate_id.setter
    def certificate_id(self, value):
        self._certificate_id = value

    @hybrid_property
    def domain_name(self):
        return self._domain_name

    @domain_name.setter
    def domain_name(self, value):
        self._domain_name = value

    @hybrid_property
    def certificate_type(self):
        return self._certificate_type

    @certificate_type.setter
    def certificate_type(self, value):
        self._certificate_type = value

    @hybrid_property
    def certificate_status(self):
        return self._certificate_status

    @certificate_status.setter
    def certificate_status(self, value):
        self._certificate_status = value

    @hybrid_property
    def is_in_use(self):
        return self._is_in_use

    @is_in_use.setter
    def is_in_use(self, value):
        self._is_in_use = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"certificate_id='{self._certificate_id}', " \
               f"domain_name='{self._domain_name}', " \
               f"certificate_type='{self._certificate_type}', " \
               f"certificate_status='{self._certificate_status}', " \
               f"is_in_use='{self._is_in_use}', " \
               f"create_time={self._create_time})>"