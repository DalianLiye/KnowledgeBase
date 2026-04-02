from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def create_engine_ora(hostname, port, service_name, username, password):
    engine = create_engine(f"oracle+oracledb://{username}:{password}@{hostname}:{port}/{service_name}")
    print('创建Oracle DB engine成功!')
    return engine


def create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    print('创建Oracle DB session成功!')
    return session


def truncate_table(session, table_name):
    truncate_sql = text(f"truncate table {table_name} ")
    session.execute(truncate_sql)
    print(f"truncate {table_name} 表成功!")


def delete_table(session, table_name, account_id):
    v_table_name = table_name.__tablename__
    session.query(table_name).filter(table_name.account_id == account_id).delete()
    session.commit()
    print(f"delete {v_table_name} 表数据成功!")


def insert_table(session, table_name, records):
    v_table_name = table_name.__tablename__
    for rec in records:
        rec_attributes = {key: getattr(rec, key) for key in dir(rec) if
                          not key.startswith('_') and not callable(getattr(rec, key))}

        new_record = table_name(**rec_attributes)
        session.add(new_record)
    session.commit()
    print(f"插入 {v_table_name} 表数据成功!")