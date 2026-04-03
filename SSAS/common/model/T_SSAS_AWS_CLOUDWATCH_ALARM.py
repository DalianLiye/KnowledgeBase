from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_CLOUDWATCH_ALARM(Base):
    __tablename__ = 'SSAS_AWS_CLOUDWATCH_ALARM'

    _account_id = Column("account_id", String, primary_key=True)
    _alarm_name = Column("alarm_name", String, primary_key=True)
    _alarm_state = Column("alarm_state", String)
    _alarm_condition = Column("alarm_condition", String)
    _alarm_action = Column("alarm_action", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def alarm_name(self):
        return self._alarm_name

    @alarm_name.setter
    def alarm_name(self, value):
        self._alarm_name = value

    @hybrid_property
    def alarm_state(self):
        return self._alarm_state

    @alarm_state.setter
    def alarm_state(self, value):
        self._alarm_state = value

    @hybrid_property
    def alarm_condition(self):
        return self._alarm_condition

    @alarm_condition.setter
    def alarm_condition(self, value):
        self._alarm_condition = value

    @hybrid_property
    def alarm_action(self):
        return self._alarm_action

    @alarm_action.setter
    def alarm_action(self, value):
        self._alarm_action = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(" \
               f"account_id='{self._account_id}', "\
               f"alarm_name='{self._alarm_name}', "\
               f"alarm_state='{self._alarm_state}', "\
               f"alarm_condition='{self._alarm_condition}', "\
               f"alarm_action='{self._alarm_action}', "\
               f"create_time={self._create_time})>"
        