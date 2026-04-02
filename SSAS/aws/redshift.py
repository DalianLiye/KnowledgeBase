from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_REDSHIFT import T_SSAS_AWS_REDSHIFT
from common.model.T_SSAS_AWS_REDSHIFT_SUBNET_GROUP import T_SSAS_AWS_REDSHIFT_SUBNET_GROUP
from common.model.T_SSAS_AWS_REDSHIFT_PARAM_GROUP import T_SSAS_AWS_REDSHIFT_PARAM_GROUP


def execute(account_id, session, **credential_key):
    redshift_client = clients.get_client_by_key('redshift', **credential_key)

    t_ssas_aws_redshift_records = []
    clusters = []
    marker = None

    while True:
        if marker:
            response = redshift_client.describe_clusters(Marker=marker)
        else:
            response = redshift_client.describe_clusters()

        clusters.extend(response.get('Clusters', []))
        marker = response.get('Marker')

        if not marker:
            break

    for cluster in clusters:
        t_ssas_aws_redshift = T_SSAS_AWS_REDSHIFT()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_redshift.account_id = account_id
        t_ssas_aws_redshift.cluster_name = cluster.get('ClusterIdentifier')
        t_ssas_aws_redshift.create_time = current_datetime
        t_ssas_aws_redshift_records.append(t_ssas_aws_redshift)

    t_ssas_aws_redshift_subnet_group_records = []
    subnet_grp_paginator = redshift_client.get_paginator('describe_cluster_subnet_groups')
    for page in subnet_grp_paginator.paginate():
        for subnet_group in page['ClusterSubnetGroups']:
            t_ssas_aws_redshift_subnet_group = T_SSAS_AWS_REDSHIFT_SUBNET_GROUP()
            current_datetime = datetime.datetime.now()

            t_ssas_aws_redshift_subnet_group.account_id = account_id
            t_ssas_aws_redshift_subnet_group.subnet_group_name = subnet_group['ClusterSubnetGroupName']
            t_ssas_aws_redshift_subnet_group.subnet_group_status = subnet_group.get('SubnetGroupStatus', 'N/A')
            t_ssas_aws_redshift_subnet_group.vpc_id = subnet_group.get('VpcId', 'N/A')
            t_ssas_aws_redshift_subnet_group.create_time = current_datetime
            t_ssas_aws_redshift_subnet_group_records.append(t_ssas_aws_redshift_subnet_group)

    t_ssas_aws_redshift_param_group_records = []
    param_grp_paginator = redshift_client.get_paginator('describe_cluster_parameter_groups')
    for page in param_grp_paginator.paginate():
        for parameter_group in page['ParameterGroups']:
            t_ssas_aws_redshift_param_group = T_SSAS_AWS_REDSHIFT_PARAM_GROUP()
            current_datetime = datetime.datetime.now()

            t_ssas_aws_redshift_param_group.account_id = account_id
            t_ssas_aws_redshift_param_group.param_group_name = parameter_group['ParameterGroupName']
            t_ssas_aws_redshift_param_group.create_time = current_datetime
            t_ssas_aws_redshift_param_group_records.append(t_ssas_aws_redshift_param_group)

    oracle.delete_table(session, T_SSAS_AWS_REDSHIFT, account_id)
    oracle.insert_table(session, T_SSAS_AWS_REDSHIFT, t_ssas_aws_redshift_records)

    oracle.delete_table(session, T_SSAS_AWS_REDSHIFT_SUBNET_GROUP, account_id)
    oracle.insert_table(session,
                        T_SSAS_AWS_REDSHIFT_SUBNET_GROUP,
                        t_ssas_aws_redshift_subnet_group_records)

    oracle.delete_table(session, T_SSAS_AWS_REDSHIFT_PARAM_GROUP, account_id)
    oracle.insert_table(session,
                        T_SSAS_AWS_REDSHIFT_PARAM_GROUP,
                        t_ssas_aws_redshift_param_group_records)

    return 0