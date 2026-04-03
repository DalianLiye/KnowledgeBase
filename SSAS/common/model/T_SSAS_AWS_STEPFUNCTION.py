from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_STEPFUNCTION(Base):
    __tablename__ = 'SSAS_AWS_STEPFUNCTION'

    _account_id = Column("account_id", String, primary_key=True)
    _state_machine_name = Column("state_machine_name", String, primary_key=True)
    _state_machine_type = Column("state_machine_type", String)
    _state_machine_status = Column("state_machine_status", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def state_machine_name(self):
        return self._state_machine_name

    @state_machine_name.setter
    def state_machine_name(self, value):
        self._state_machine_name = value

    @hybrid_property
    def state_machine_type(self):
        return self._state_machine_type

    @state_machine_type.setter
    def state_machine_type(self, value):
        self._state_machine_type = value

    @hybrid_property
    def state_machine_status(self):
        return self._state_machine_status

    @state_machine_status.setter
    def state_machine_status(self, value):
        self._state_machine_status = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id={self.account_id}, " \
               f"state_machine_name='{self.state_machine_name}', " \
               f"state_machine_type='{self.state_machine_type}', " \
               f"state_machine_status='{self.state_machine_status}', " \
               f"create_time={self.create_time})>"