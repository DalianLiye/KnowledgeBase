from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_ACCOUNT import T_SSAS_AWS_ACCOUNT


def execute(env, session, **credential_key):

    sts_client = clients.get_client_by_key('sts', **credential_key)

    t_ssas_aws_account_records = []

    response = sts_client.get_caller_identity()
    account_id = response['Account']

    if account_id == '405248615330':
        account_name = 'mccn-cd-hhie'
    elif account_id == '028968471271':
        account_name = 'mccn-dit-hhie'
    elif account_id == '028956411062':
        account_name = 'mccn-diu-hhie'
    elif account_id == '029003244739':
        account_name = 'mccn-dip-hhie'

    t_ssas_aws_account = T_SSAS_AWS_ACCOUNT()
    current_datetime = datetime.datetime.now()

    t_ssas_aws_account.env = env
    t_ssas_aws_account.account_id = account_id
    t_ssas_aws_account.account_name = account_name
    t_ssas_aws_account.create_time = current_datetime
    t_ssas_aws_account_records.append(t_ssas_aws_account)

    oracle.delete_table(session, T_SSAS_AWS_ACCOUNT, account_id)
    oracle.insert_table(session, T_SSAS_AWS_ACCOUNT, t_ssas_aws_account_records)

    return 0