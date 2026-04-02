from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_IAM_ROLE import T_SSAS_AWS_IAM_ROLE
from common.model.T_SSAS_AWS_IAM_USER import T_SSAS_AWS_IAM_USER


def execute(account_id, session, **credential_key):

    iam_client = clients.get_client_by_key('iam', **credential_key)
    response_user = iam_client.list_users()

    t_ssas_aws_iam_user_records = []

    for user in response_user['Users']:

        t_ssas_aws_iam_user = T_SSAS_AWS_IAM_USER()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_iam_user.account_id = account_id
        t_ssas_aws_iam_user.iam_user_name = user['UserName']
        t_ssas_aws_iam_user.create_time = current_datetime
        t_ssas_aws_iam_user_records.append(t_ssas_aws_iam_user)

    response_role = iam_client.list_roles()
    t_ssas_aws_iam_role_records = []

    for role in response_role['Roles']:

        t_ssas_aws_iam_role = T_SSAS_AWS_IAM_ROLE()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_iam_role.account_id = account_id
        t_ssas_aws_iam_role.iam_role_name = role['RoleName']
        t_ssas_aws_iam_role.create_time = current_datetime
        t_ssas_aws_iam_role_records.append(t_ssas_aws_iam_role)

    oracle.delete_table(session, T_SSAS_AWS_IAM_USER, account_id)
    oracle.insert_table(session, T_SSAS_AWS_IAM_USER, t_ssas_aws_iam_user_records)
    oracle.delete_table(session, T_SSAS_AWS_IAM_ROLE, account_id)
    oracle.insert_table(session, T_SSAS_AWS_IAM_ROLE, t_ssas_aws_iam_role_records)

    return 0