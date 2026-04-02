from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_SNS import T_SSAS_AWS_SNS


def execute(account_id, session, **credential_key):

    sns_client = clients.get_client_by_key('sns', **credential_key)

    t_ssas_aws_sns_records = []
    topics = []
    next_token = None

    while True:
        if next_token:
            response = sns_client.list_topics(NextToken=next_token)
        else:
            response = sns_client.list_topics()

        topics.extend(response.get('Topics', []))
        next_token = response.get('NextToken')

        if not next_token:
            break

    for topic in topics:
        t_ssas_aws_sns = T_SSAS_AWS_SNS()
        current_datetime = datetime.datetime.now()
        topic_name = topic['TopicArn'].split(':')[-1]

        t_ssas_aws_sns.account_id = account_id
        t_ssas_aws_sns.topic_name = topic_name
        t_ssas_aws_sns.create_time = current_datetime
        t_ssas_aws_sns_records.append(t_ssas_aws_sns)

    oracle.delete_table(session, T_SSAS_AWS_SNS, account_id)
    oracle.insert_table(session, T_SSAS_AWS_SNS, t_ssas_aws_sns_records)

    return 0