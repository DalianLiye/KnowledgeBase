from common.connection.aws import clients
from common.connection.db import oracle
from common.model.T_SSAS_AWS_VPC import T_SSAS_AWS_VPC
from common.model.T_SSAS_AWS_VPC_SUBNET import T_SSAS_AWS_VPC_SUBNET
import datetime


def get_instance_name(instance):
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            return tag['Value']
    return None


def execute(account_id, session, **credential_key):

    ec2_client = clients.get_client_by_key('ec2', **credential_key)

    t_ssas_aws_vpc_records = []
    t_ssas_aws_vpc_subnet_records = []

    response = ec2_client.describe_vpcs()
    for vpc in response['Vpcs']:

        t_ssas_aws_vpc = T_SSAS_AWS_VPC()
        current_datetime = datetime.datetime.now()
        vpc_id = vpc['VpcId']
        vpc_name = 'N/A'
        if 'Tags' in vpc:
            for tag in vpc['Tags']:
                if tag['Key'] == 'Name':
                    vpc_name = tag['Value']
                    break

        t_ssas_aws_vpc.account_id = account_id
        t_ssas_aws_vpc.vpc_id = vpc_id
        t_ssas_aws_vpc.vpc_name = vpc_name
        t_ssas_aws_vpc.create_time = current_datetime
        t_ssas_aws_vpc_records.append(t_ssas_aws_vpc)

    response = ec2_client.describe_subnets()
    for subnet in response['Subnets']:

        t_ssas_aws_vpc_subnet = T_SSAS_AWS_VPC_SUBNET()
        vpc_id = subnet['VpcId']
        subnet_id = subnet['SubnetId']
        subnet_name = 'N/A'
        if 'Tags' in subnet:
            for tag in subnet['Tags']:
                if tag['Key'] == 'Name':
                    subnet_name = tag['Value']
                    break

        t_ssas_aws_vpc_subnet.account_id = account_id
        t_ssas_aws_vpc_subnet.vpc_id = vpc_id
        t_ssas_aws_vpc_subnet.subnet_id = subnet_id
        t_ssas_aws_vpc_subnet.subnet_name = subnet_name
        t_ssas_aws_vpc_subnet.create_time = current_datetime
        t_ssas_aws_vpc_subnet_records.append(t_ssas_aws_vpc_subnet)

    oracle.delete_table(session, T_SSAS_AWS_VPC, account_id)
    oracle.insert_table(session, T_SSAS_AWS_VPC, t_ssas_aws_vpc_records)
    oracle.delete_table(session, T_SSAS_AWS_VPC_SUBNET, account_id)
    oracle.insert_table(session, T_SSAS_AWS_VPC_SUBNET, t_ssas_aws_vpc_subnet_records)

    return 0