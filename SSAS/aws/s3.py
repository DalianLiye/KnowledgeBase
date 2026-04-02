from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_S3 import T_SSAS_AWS_S3


def execute(account_id, session, **credential_key):

    s3_client = clients.get_client_by_key('s3', **credential_key)
    response = s3_client.list_buckets()

    t_ssas_aws_s3_records = []
    eight_hours = datetime.timedelta(hours=8)

    for bucket in response['Buckets']:

        t_ssas_aws_s3 = T_SSAS_AWS_S3()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_s3.account_id = account_id
        t_ssas_aws_s3.bucket_name = 's3://' + bucket["Name"]
        t_ssas_aws_s3.bucket_creation_date = bucket["CreationDate"] + eight_hours
        t_ssas_aws_s3.bucket_description = ''
        t_ssas_aws_s3.create_time = current_datetime
        t_ssas_aws_s3_records.append(t_ssas_aws_s3)

    oracle.delete_table(session, T_SSAS_AWS_S3, account_id)
    oracle.insert_table(session, T_SSAS_AWS_S3, t_ssas_aws_s3_records)

    return 0