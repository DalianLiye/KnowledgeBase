from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_STEPFUNCTION import T_SSAS_AWS_STEPFUNCTION


def execute(account_id, session, **credential_key):

    stepfunction_client = clients.get_client_by_key('stepfunctions', **credential_key)

    t_ssas_aws_stepfunction_records = []
    paginator = stepfunction_client.get_paginator('list_state_machines')

    for page in paginator.paginate():
        for state_machine in page['stateMachines']:

            t_ssas_aws_stepfunction = T_SSAS_AWS_STEPFUNCTION()
            state_machine_arn = state_machine['stateMachineArn']
            state_machine_details = stepfunction_client.describe_state_machine(stateMachineArn=state_machine_arn)
            current_datetime = datetime.datetime.now()

            t_ssas_aws_stepfunction.account_id = account_id
            t_ssas_aws_stepfunction.state_machine_name = state_machine['name']
            t_ssas_aws_stepfunction.state_machine_type = state_machine_details['type']
            t_ssas_aws_stepfunction.state_machine_status = state_machine_details['status']
            t_ssas_aws_stepfunction.create_time = current_datetime
            t_ssas_aws_stepfunction_records.append(t_ssas_aws_stepfunction)

    oracle.delete_table(session, T_SSAS_AWS_STEPFUNCTION, account_id)
    oracle.insert_table(session, T_SSAS_AWS_STEPFUNCTION, t_ssas_aws_stepfunction_records)

    return 0