from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_SQS import T_SSAS_AWS_SQS


def execute(account_id, session, **credential_key):

    sqs_client = clients.get_client_by_key('sqs', **credential_key)
    response = sqs_client.list_queues()
    queue_urls = response.get('QueueUrls', [])

    queue_names = [queue_url.split('/')[-1] for queue_url in queue_urls]

    t_ssas_aws_sqs_records = []
    for queue_name in queue_names:

        t_ssas_aws_sqs = T_SSAS_AWS_SQS()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_sqs.account_id = account_id
        t_ssas_aws_sqs.sqs_name = queue_name
        t_ssas_aws_sqs.create_time = current_datetime
        t_ssas_aws_sqs_records.append(t_ssas_aws_sqs)

    oracle.delete_table(session, T_SSAS_AWS_SQS, account_id)
    oracle.insert_table(session, T_SSAS_AWS_SQS, t_ssas_aws_sqs_records)

    return 0