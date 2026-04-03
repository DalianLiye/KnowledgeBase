from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_CLOUDWATCH_LOG(Base):
    __tablename__ = 'SSAS_AWS_CLOUDWATCH_LOG'

    _account_id = Column("account_id", String, primary_key=True)
    _log_group_name = Column("log_group_name", String, primary_key=True)
    _log_class = Column("log_class", String)
    _retention = Column("retention", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def log_group_name(self):
        return self._log_group_name

    @log_group_name.setter
    def log_group_name(self, value):
        self._log_group_name = value

    @hybrid_property
    def log_class(self):
        return self._log_class

    @log_class.setter
    def log_class(self, value):
        self._log_class = value

    @hybrid_property
    def retention(self):
        return self._retention

    @retention.setter
    def retention(self, value):
        self._retention = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"log_group_name='{self._log_group_name}', " \
               f"log_class='{self._log_class}', " \
               f"retention='{self._retention}', " \
               f"create_time={self._create_time})>"