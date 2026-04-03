from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class T_SSAS_AWS_EC2(Base):
    __tablename__ = 'SSAS_AWS_EC2'

    _account_id = Column("account_id", String, primary_key=True)
    _ec2_instance_id = Column("ec2_instance_id", String, primary_key=True)
    _ec2_instance_name = Column("ec2_instance_name", String)
    _ec2_instance_state = Column("ec2_instance_state", String)
    _ec2_instance_type = Column("ec2_instance_type", String)
    _ec2_instance_platform = Column("ec2_instance_platform", String)
    _create_time = Column("create_time", TIMESTAMP)

    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def ec2_instance_id(self):
        return self._ec2_instance_id

    @ec2_instance_id.setter
    def ec2_instance_id(self, value):
        self._ec2_instance_id = value

    @hybrid_property
    def ec2_instance_name(self):
        return self._ec2_instance_name

    @ec2_instance_name.setter
    def ec2_instance_name(self, value):
        self._ec2_instance_name = value

    @hybrid_property
    def ec2_instance_state(self):
        return self._ec2_instance_state

    @ec2_instance_state.setter
    def ec2_instance_state(self, value):
        self._ec2_instance_state = value

    @hybrid_property
    def ec2_instance_type(self):
        return self._ec2_instance_type

    @ec2_instance_type.setter
    def ec2_instance_type(self, value):
        self._ec2_instance_type = value

    @hybrid_property
    def ec2_instance_platform(self):
        return self._ec2_instance_platform

    @ec2_instance_platform.setter
    def ec2_instance_platform(self, value):
        self._ec2_instance_platform = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return f"<MyTable(account_id='{self._account_id}', " \
               f"ec2_instance_id='{self._ec2_instance_id}', " \
               f"ec2_instance_name='{self._ec2_instance_name}', " \
               f"ec2_instance_state='{self._ec2_instance_state}', " \
               f"ec2_instance_type='{self._ec2_instance_type}', " \
               f"ec2_instance_platform='{self._ec2_instance_platform}', " \
               f"create_time={self._create_time})>"