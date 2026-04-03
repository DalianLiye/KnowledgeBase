from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_RDS(Base):
    __tablename__ = 'SSAS_AWS_RDS'

    _account_id = Column("account_id", String, primary_key=True)
    _db_identifier = Column("db_identifier", String, primary_key=True)
    _db_class = Column("db_class", String)
    _db_engine = Column("db_engine", String)
    _db_engine_version = Column("db_engine_version", String)
    _db_state = Column("db_state", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def db_identifier(self):
        return self._db_identifier

    @db_identifier.setter
    def db_identifier(self, value):
        self._db_identifier = value

    @hybrid_property
    def db_class(self):
        return self._db_class

    @db_class.setter
    def db_class(self, value):
        self._db_class = value

    @hybrid_property
    def db_engine(self):
        return self._db_engine

    @db_engine.setter
    def db_engine(self, value):
        self._db_engine = value

    @hybrid_property
    def db_engine_version(self):
        return self._db_engine_version

    @db_engine_version.setter
    def db_engine_version(self, value):
        self._db_engine_version = value

    @hybrid_property
    def db_state(self):
        return self._db_state

    @db_state.setter
    def db_state(self, value):
        self._db_state = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"db_identifier='{self._db_identifier}', " \
               f"db_class='{self._db_class}', " \
               f"db_engine='{self._db_engine}', " \
               f"db_engine_version='{self._db_engine_version}', " \
               f"db_state='{self._db_state}', " \
               f"create_time={self._create_time})>"