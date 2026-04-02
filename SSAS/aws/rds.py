from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_RDS import T_SSAS_AWS_RDS


def execute(account_id, session, **credential_key):

    rds_client = clients.get_client_by_key('rds', **credential_key)
    response = rds_client.describe_db_instances()

    t_ssas_aws_rds_records = []

    for instance in response['DBInstances']:

        t_ssas_aws_rds = T_SSAS_AWS_RDS()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_rds.account_id = account_id
        t_ssas_aws_rds.db_identifier = instance['DBInstanceIdentifier']
        t_ssas_aws_rds.db_class = instance['DBInstanceClass']
        t_ssas_aws_rds.db_engine = instance['Engine']
        t_ssas_aws_rds.db_engine_version = instance['EngineVersion']
        t_ssas_aws_rds.db_state = instance['DBInstanceStatus']
        t_ssas_aws_rds.create_time = current_datetime
        t_ssas_aws_rds_records.append(t_ssas_aws_rds)

    oracle.delete_table(session, T_SSAS_AWS_RDS, account_id)
    oracle.insert_table(session, T_SSAS_AWS_RDS, t_ssas_aws_rds_records)

    return 0