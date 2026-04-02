from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_SSM_PARAM import T_SSAS_AWS_SSM_PARAM


def execute(account_id, session, **credential_key):

    ssm_client = clients.get_client_by_key('ssm', **credential_key)

    t_ssas_aws_ssm_param_records = []
    paginator = ssm_client.get_paginator('describe_parameters')

    for page in paginator.paginate():
        for parameter in page['Parameters']:
            t_ssas_aws_ssm_param = T_SSAS_AWS_SSM_PARAM()
            current_datetime = datetime.datetime.now()

            t_ssas_aws_ssm_param.account_id = account_id
            t_ssas_aws_ssm_param.param_name = parameter['Name']
            t_ssas_aws_ssm_param.param_tier = parameter.get('Tier', 'Standard')
            t_ssas_aws_ssm_param.param_type = parameter['Type']
            t_ssas_aws_ssm_param.create_time = current_datetime
            t_ssas_aws_ssm_param_records.append(t_ssas_aws_ssm_param)

    oracle.delete_table(session, T_SSAS_AWS_SSM_PARAM, account_id)
    oracle.insert_table(session, T_SSAS_AWS_SSM_PARAM, t_ssas_aws_ssm_param_records)

    return 0