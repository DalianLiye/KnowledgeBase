from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_RESOURCE_GROUP import T_SSAS_AWS_RESOURCE_GROUP


def execute(account_id, session, **credential_key):

    resourcegroups_client = clients.get_client_by_key('resource-groups', **credential_key)

    t_ssas_aws_resource_group_records = []
    paginator = resourcegroups_client.get_paginator('list_groups')

    for page in paginator.paginate():
        for group in page['Groups']:
            t_ssas_aws_resource_group = T_SSAS_AWS_RESOURCE_GROUP()
            current_datetime = datetime.datetime.now()

            t_ssas_aws_resource_group.account_id = account_id
            t_ssas_aws_resource_group.group_name = group['Name']
            t_ssas_aws_resource_group.description = group.get('Description', 'N/A')
            t_ssas_aws_resource_group.create_time = current_datetime
            t_ssas_aws_resource_group_records.append(t_ssas_aws_resource_group)

    oracle.delete_table(session, T_SSAS_AWS_RESOURCE_GROUP, account_id)
    oracle.insert_table(session, T_SSAS_AWS_RESOURCE_GROUP, t_ssas_aws_resource_group_records)

    return 0