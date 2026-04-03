from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class T_SSAS_AWS_GLUE(Base):
    __tablename__ = 'SSAS_AWS_GLUE'

    _account_id = Column("account_id", String, primary_key=True)
    _glue_name = Column("glue_name", String, primary_key=True)
    _glue_description = Column("glue_description", String)
    _glue_role = Column("glue_role", String)
    _glue_type = Column("glue_type", String)
    _glue_scriptlocation = Column("glue_scriptlocation", String)
    _glue_pythonversion = Column("glue_pythonversion", String)
    _glue_dataprocessunit = Column("glue_dataprocessunit", String)
    _glue_timeout = Column("glue_timeout", String)
    _glue_maxretries = Column("glue_maxretries", String)
    _glue_jobmode = Column("glue_jobmode", String)
    _glue_createdon = Column("glue_createdon", String)
    _glue_lastmodifiedon = Column("glue_lastmodifiedon", String)
    _glue_connections = Column("glue_connections", String)
    _glue_defaultarguments = Column("glue_defaultarguments", String)
    _glue_maxconcurrentruns = Column("glue_maxconcurrentruns", String)
    _glue_version = Column("glue_version", String)
    _create_time = Column("create_time", TIMESTAMP)

    # 以account_id为例，其他字段同理生成getter/setter
    @hybrid_property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @hybrid_property
    def glue_name(self):
        return self._glue_name

    @glue_name.setter
    def glue_name(self, value):
        self._glue_name = value

    @hybrid_property
    def glue_description(self):
        return self._glue_description

    @glue_description.setter
    def glue_description(self, value):
        self._glue_description = value

    @hybrid_property
    def glue_role(self):
        return self._glue_role

    @glue_role.setter
    def glue_role(self, value):
        self._glue_role = value

    @hybrid_property
    def glue_type(self):
        return self._glue_type

    @glue_type.setter
    def glue_type(self, value):
        self._glue_type = value

    @hybrid_property
    def glue_scriptlocation(self):
        return self._glue_scriptlocation

    @glue_scriptlocation.setter
    def glue_scriptlocation(self, value):
        self._glue_scriptlocation = value

    @hybrid_property
    def glue_pythonversion(self):
        return self._glue_pythonversion

    @glue_pythonversion.setter
    def glue_pythonversion(self, value):
        self._glue_pythonversion = value

    @hybrid_property
    def glue_dataprocessunit(self):
        return self._glue_dataprocessunit

    @glue_dataprocessunit.setter
    def glue_dataprocessunit(self, value):
        self._glue_dataprocessunit = value

    @hybrid_property
    def glue_timeout(self):
        return self._glue_timeout

    @glue_timeout.setter
    def glue_timeout(self, value):
        self._glue_timeout = value

    @hybrid_property
    def glue_maxretries(self):
        return self._glue_maxretries

    @glue_maxretries.setter
    def glue_maxretries(self, value):
        self._glue_maxretries = value

    @hybrid_property
    def glue_jobmode(self):
        return self._glue_jobmode

    @glue_jobmode.setter
    def glue_jobmode(self, value):
        self._glue_jobmode = value

    @hybrid_property
    def glue_createdon(self):
        return self._glue_createdon

    @glue_createdon.setter
    def glue_createdon(self, value):
        self._glue_createdon = value

    @hybrid_property
    def glue_lastmodifiedon(self):
        return self._glue_lastmodifiedon

    @glue_lastmodifiedon.setter
    def glue_lastmodifiedon(self, value):
        self._glue_lastmodifiedon = value

    @hybrid_property
    def glue_connections(self):
        return self._glue_connections

    @glue_connections.setter
    def glue_connections(self, value):
        self._glue_connections = value

    @hybrid_property
    def glue_defaultarguments(self):
        return self._glue_defaultarguments

    @glue_defaultarguments.setter
    def glue_defaultarguments(self, value):
        self._glue_defaultarguments = value

    @hybrid_property
    def glue_maxconcurrentruns(self):
        return self._glue_maxconcurrentruns

    @glue_maxconcurrentruns.setter
    def glue_maxconcurrentruns(self, value):
        self._glue_maxconcurrentruns = value

    @hybrid_property
    def glue_version(self):
        return self._glue_version

    @glue_version.setter
    def glue_version(self, value):
        self._glue_version = value

    @hybrid_property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, value):
        self._create_time = value

    def __repr__(self):
        return  f"<MyTable(" \
                f"account_id='{self._account_id}', "\
                f"glue_name='{self._glue_name}', "\
                f"glue_type='{self._glue_type}', "\
                f"glue_version='{self._glue_version}', "\
                f"glue_description='{self._glue_description}', "\
                f"glue_role='{self._glue_role}', "\
                f"glue_scriptlocation='{self._glue_scriptlocation}', "\
                f"glue_pythonversion='{self._glue_pythonversion}', "\
                f"glue_dataprocessunit='{self._glue_dataprocessunit}', "\
                f"glue_timeout='{self._glue_timeout}', "\
                f"glue_maxretries='{self._glue_maxretries}', "\
                f"glue_jobmode='{self._glue_jobmode}', "\
                f"glue_createdon='{self._glue_createdon}', "\
                f"glue_lastmodifiedon='{self._glue_lastmodifiedon}', "\
                f"glue_connections='{self._glue_connections}', "\
                f"glue_defaultarguments='{self._glue_defaultarguments}', "\
                f"glue_maxconcurrentruns='{self._glue_maxconcurrentruns}', "\
                f"create_time={self._create_time})>"
        