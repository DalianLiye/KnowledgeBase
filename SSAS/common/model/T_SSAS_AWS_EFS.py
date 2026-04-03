from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_EFS(Base):
    __tablename__ = 'SSAS_AWS_EFS'

    _account_id = Column("account_id", String, primary_key=True)
    _efs_name = Column("efs_name", String, primary_key=True)
    _file_system_id = Column("file_system_id", String)
    _encrypted = Column("encrypted", String)
    _total_size = Column("total_size", String)
    _performance_mode = Column("performance_mode", String)
    _throughput_mode = Column("throughput_mode", String)
    _automatic_backups = Column("automatic_backups", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def efs_name(self):
        return self._efs_name

    @efs_name.setter
    def efs_name(self, value):
        self._efs_name = value

    @hybrid_property
    def file_system_id(self):
        return self._file_system_id

    @file_system_id.setter
    def file_system_id(self, value):
        self._file_system_id = value

    @hybrid_property
    def encrypted(self):
        return self._encrypted

    @encrypted.setter
    def encrypted(self, value):
        self._encrypted = value

    @hybrid_property
    def total_size(self):
        return self._total_size

    @total_size.setter
    def total_size(self, value):
        self._total_size = value

    @hybrid_property
    def performance_mode(self):
        return self._performance_mode

    @performance_mode.setter
    def performance_mode(self, value):
        self._performance_mode = value

    @hybrid_property
    def throughput_mode(self):
        return self._throughput_mode

    @throughput_mode.setter
    def throughput_mode(self, value):
        self._throughput_mode = value

    @hybrid_property
    def automatic_backups(self):
        return self._automatic_backups

    @automatic_backups.setter
    def automatic_backups(self, value):
        self._automatic_backups = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"efs_name='{self._efs_name}', " \
               f"file_system_id='{self._file_system_id}', " \
               f"encrypted='{self._encrypted}', " \
               f"total_size='{self._total_size}', " \
               f"performance_mode='{self._performance_mode}', " \
               f"throughput_mode='{self._throughput_mode}', " \
               f"automatic_backups='{self._automatic_backups}', " \
               f"create_time={self._create_time})>"