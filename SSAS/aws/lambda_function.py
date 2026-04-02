from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_LAMBDA import T_SSAS_AWS_LAMBDA


def execute(account_id, session, **credential_key):

    lambda_client = clients.get_client_by_key('lambda', **credential_key)
    response = lambda_client.list_functions()

    t_ssas_aws_lambda_records = []

    for instance in response['Functions']:

        t_ssas_aws_lambda = T_SSAS_AWS_LAMBDA()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_lambda.account_id = account_id
        t_ssas_aws_lambda.lambda_name = instance['FunctionName']
        t_ssas_aws_lambda.create_time = current_datetime
        t_ssas_aws_lambda_records.append(t_ssas_aws_lambda)

    oracle.delete_table(session, T_SSAS_AWS_LAMBDA, account_id)
    oracle.insert_table(session, T_SSAS_AWS_LAMBDA, t_ssas_aws_lambda_records)

    return 0