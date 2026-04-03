from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_ACM_CERTIFICATE_ASSOCIATE(Base):
    __tablename__ = 'SSAS_AWS_ACM_CERTIFICATE_ASSOCIATE'

    _account_id = Column("account_id", String, primary_key=True)
    _certificate_id = Column("certificate_id", String, primary_key=True)
    _associate_arn = Column("associate_arn", String)
    _associate_type = Column("associate_type", String)
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
    def associate_arn(self):
        return self._associate_arn

    @associate_arn.setter
    def associate_arn(self, value):
        self._associate_arn = value

    @hybrid_property
    def associate_type(self):
        return self._associate_type

    @associate_type.setter
    def associate_type(self, value):
        self._associate_type = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(" \
               f"account_id='{self._account_id}', "\
               f"certificate_id='{self._certificate_id}', "\
               f"associate_arn='{self._associate_arn}', "\
               f"associate_type='{self._associate_type}', "\
               f"create_time={self._create_time})>"
        