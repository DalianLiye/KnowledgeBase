from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_DYNAMODB import T_SSAS_AWS_DYNAMODB


def execute(account_id, session, **credential_key):

    dynamodb_client = clients.get_client_by_key('dynamodb', **credential_key)

    t_ssas_aws_dynamodb_records = []
    tables = []
    last_evaluated_table_name = None

    while True:
        if last_evaluated_table_name:
            response = dynamodb_client.list_tables(ExclusiveStartTableName=last_evaluated_table_name)
        else:
            response = dynamodb_client.list_tables()

        tables.extend(response.get('TableNames', []))
        last_evaluated_table_name = response.get('LastEvaluatedTableName')

        if not last_evaluated_table_name:
            break

    for table_name in tables:

        t_ssas_aws_dynamodb = T_SSAS_AWS_DYNAMODB()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_dynamodb.account_id = account_id
        t_ssas_aws_dynamodb.table_name = table_name
        t_ssas_aws_dynamodb.create_time = current_datetime
        t_ssas_aws_dynamodb_records.append(t_ssas_aws_dynamodb)

    oracle.delete_table(session, T_SSAS_AWS_DYNAMODB, account_id)
    oracle.insert_table(session, T_SSAS_AWS_DYNAMODB, t_ssas_aws_dynamodb_records)

    return 0