from common.connection.aws import clients
from common.connection.db import oracle
from common.model.T_SSAS_AWS_EC2 import T_SSAS_AWS_EC2
import datetime


def get_instance_name(instance):
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            return tag['Value']
    return None


def execute(account_id, session, **credential_key):

    ec2_client = clients.get_client_by_key('ec2', **credential_key)
    t_ssas_aws_ec2_records = []

    response = ec2_client.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:

            t_ssas_aws_ec2 = T_SSAS_AWS_EC2()
            name = get_instance_name(instance)
            current_datetime = datetime.datetime.now()

            t_ssas_aws_ec2.account_id = account_id
            t_ssas_aws_ec2.ec2_instance_id = instance['InstanceId']
            t_ssas_aws_ec2.ec2_instance_name = name
            t_ssas_aws_ec2.ec2_instance_state = instance['State']['Name']
            t_ssas_aws_ec2.ec2_instance_type = instance['InstanceType']
            t_ssas_aws_ec2.ec2_instance_platform = instance.get('PlatformDetails', 'N/A')
            t_ssas_aws_ec2.create_time = current_datetime
            t_ssas_aws_ec2_records.append(t_ssas_aws_ec2)

    oracle.delete_table(session, T_SSAS_AWS_EC2, account_id)
    oracle.insert_table(session, T_SSAS_AWS_EC2, t_ssas_aws_ec2_records)

    return 0