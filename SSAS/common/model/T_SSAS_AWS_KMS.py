from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_KMS(Base):
    __tablename__ = 'SSAS_AWS_KMS'

    _account_id = Column("account_id", String, primary_key=True)
    _key_alias = Column("key_alias", String, primary_key=True)
    _key_id = Column("key_id", String)
    _key_manager = Column("key_manager", String)
    _key_status = Column("key_status", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def key_alias(self):
        return self._key_alias

    @key_alias.setter
    def key_alias(self, value):
        self._key_alias = value

    @hybrid_property
    def key_id(self):
        return self._key_id

    @key_id.setter
    def key_id(self, value):
        self._key_id = value

    @hybrid_property
    def key_manager(self):
        return self._key_manager

    @key_manager.setter
    def key_manager(self, value):
        self._key_manager = value

    @hybrid_property
    def key_status(self):
        return self._key_status

    @key_status.setter
    def key_status(self, value):
        self._key_status = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"key_alias='{self._key_alias}', " \
               f"key_id='{self._key_id}', " \
               f"key_manager='{self._key_manager}', " \
               f"key_status='{self._key_status}', " \
               f"create_time={self._create_time})>"