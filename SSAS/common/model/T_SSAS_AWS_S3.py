from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_S3(Base):
    __tablename__ = 'SSAS_AWS_S3'

    _account_id = Column("account_id", String, primary_key=True)
    _bucket_name = Column("bucket_name", String, primary_key=True)
    _bucket_creation_date = Column("bucket_creation_date", TIMESTAMP)
    _bucket_description = Column("bucket_description", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def bucket_name(self):
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, value):
        self._bucket_name = value

    @hybrid_property
    def bucket_creation_date(self):
        return self._bucket_creation_date

    @bucket_creation_date.setter
    def bucket_creation_date(self, value):
        self._bucket_creation_date = value

    @hybrid_property
    def bucket_description(self):
        return self._bucket_description

    @bucket_description.setter
    def bucket_description(self, value):
        self._bucket_description = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"bucket_name='{self._bucket_name}', " \
               f"bucket_creation_date='{self._bucket_creation_date}', " \
               f"bucket_description='{self._bucket_description}', " \
               f"create_time={self._create_time})>"