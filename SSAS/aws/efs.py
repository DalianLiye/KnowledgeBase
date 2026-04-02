from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_EFS import T_SSAS_AWS_EFS


def execute(account_id, session, **credential_key):

    efs_client = clients.get_client_by_key('efs', **credential_key)

    t_ssas_aws_efs_records = []

    paginator = efs_client.get_paginator('describe_file_systems')
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for fs in page['FileSystems']:
            t_ssas_aws_efs = T_SSAS_AWS_EFS()
            current_datetime = datetime.datetime.now()
            efs_name = ''
            if 'Tags' in fs:
                efs_name_tag = [tag['Value'] for tag in fs['Tags'] if tag['Key'] == 'Name']
                efs_name = efs_name_tag[0] if efs_name_tag else ''

            t_ssas_aws_efs.account_id = account_id
            t_ssas_aws_efs.efs_name  = efs_name
            t_ssas_aws_efs.file_system_id = fs.get('FileSystemId', '')
            t_ssas_aws_efs.encrypted = str(fs.get('Encrypted', ''))
            t_ssas_aws_efs.total_size = str(fs.get('SizeInBytes', {}).get('Value', '')) + " Bytes"
            t_ssas_aws_efs.performance_mode = fs.get('PerformanceMode', '')
            t_ssas_aws_efs.throughput_mode = fs.get('ThroughputMode', '')
            t_ssas_aws_efs.automatic_backups = str(fs.get('BackupPolicy', {}).get('Status', '') == 'ENABLED') if 'BackupPolicy' in fs else 'False'
            t_ssas_aws_efs.create_time = current_datetime
            t_ssas_aws_efs_records.append(t_ssas_aws_efs)

    oracle.delete_table(session, T_SSAS_AWS_EFS, account_id)
    oracle.insert_table(session, T_SSAS_AWS_EFS, t_ssas_aws_efs_records)

    return 0