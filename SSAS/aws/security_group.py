from common.connection.aws import clients
from common.connection.db import oracle
from common.model.T_SSAS_AWS_EC2_SG import T_SSAS_AWS_EC2_SG
import datetime


def execute(account_id, session, **credential_key):

    ec2_client = clients.get_client_by_key('ec2', **credential_key)
    t_ssas_aws_ec2_sg_records = []

    paginator = ec2_client.get_paginator('describe_security_groups')
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for sg in page['SecurityGroups']:
            t_ssas_aws_ec2_sg = T_SSAS_AWS_EC2_SG()
            current_datetime = datetime.datetime.now()

            t_ssas_aws_ec2_sg.account_id = account_id
            t_ssas_aws_ec2_sg.vpc_id = sg['VpcId'] if 'VpcId' in sg else 'N/A'
            t_ssas_aws_ec2_sg.security_group_id = sg['GroupId']
            t_ssas_aws_ec2_sg.security_group_name = sg['GroupName']
            t_ssas_aws_ec2_sg.security_group_description = sg['Description']
            t_ssas_aws_ec2_sg.create_time = current_datetime
            t_ssas_aws_ec2_sg_records.append(t_ssas_aws_ec2_sg)

    oracle.delete_table(session, T_SSAS_AWS_EC2_SG, account_id)
    oracle.insert_table(session, T_SSAS_AWS_EC2_SG, t_ssas_aws_ec2_sg_records)

    return 0