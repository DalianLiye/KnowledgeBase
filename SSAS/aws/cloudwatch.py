from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_CLOUDWATCH_ALARM import T_SSAS_AWS_CLOUDWATCH_ALARM
from common.model.T_SSAS_AWS_CLOUDWATCH_LOG import T_SSAS_AWS_CLOUDWATCH_LOG


def execute(account_id, session, **credential_key):

    cloudwatch_client = clients.get_client_by_key('cloudwatch', **credential_key)

    t_ssas_aws_cloudwatch_alarm_records = []

    paginator = cloudwatch_client.get_paginator('describe_alarms')

    all_alarms = []
    for page in paginator.paginate():
        all_alarms.extend(page['MetricAlarms'])

    for alarm in all_alarms:

        comparison_operator = alarm.get('ComparisonOperator')
        threshold = alarm.get('Threshold')
        evaluation_periods = alarm.get('EvaluationPeriods')
        metric_name = alarm.get('MetricName')
        namespace = alarm.get('Namespace')
        alarm_actions = alarm.get('AlarmActions', [])

        t_ssas_aws_cloudwatch_alarm = T_SSAS_AWS_CLOUDWATCH_ALARM()
        current_datetime = datetime.datetime.now()
        t_ssas_aws_cloudwatch_alarm.account_id = account_id
        t_ssas_aws_cloudwatch_alarm.alarm_name = alarm['AlarmName']
        t_ssas_aws_cloudwatch_alarm.alarm_state = alarm['StateValue']
        t_ssas_aws_cloudwatch_alarm.alarm_condition = f"Condition: ComparisonOperator={comparison_operator}, Threshold={threshold}, EvaluationPeriods={evaluation_periods}, MetricName={metric_name}, Namespace={namespace}"
        t_ssas_aws_cloudwatch_alarm.alarm_action = f"Actions: {', '.join(alarm_actions) if alarm_actions else 'No Actions'}"
        t_ssas_aws_cloudwatch_alarm.create_time = current_datetime
        t_ssas_aws_cloudwatch_alarm_records.append(t_ssas_aws_cloudwatch_alarm)

    cloudwatch_logs_client = clients.get_client_by_key('logs', **credential_key)

    t_ssas_aws_cloudwatch_logs_records = []

    paginator = cloudwatch_logs_client.get_paginator('describe_log_groups')

    for page in paginator.paginate():
        for log_group in page['logGroups']:

            t_ssas_aws_cloudwatch_log = T_SSAS_AWS_CLOUDWATCH_LOG()
            current_datetime = datetime.datetime.now()

            t_ssas_aws_cloudwatch_log.account_id = account_id
            t_ssas_aws_cloudwatch_log.log_group_name = log_group['logGroupName']
            t_ssas_aws_cloudwatch_log.log_class = log_group['logGroupClass']
            t_ssas_aws_cloudwatch_log.retention = ''
            t_ssas_aws_cloudwatch_log.create_time = current_datetime
            t_ssas_aws_cloudwatch_logs_records.append(t_ssas_aws_cloudwatch_log)

    oracle.delete_table(session, T_SSAS_AWS_CLOUDWATCH_ALARM, account_id)
    oracle.insert_table(session, T_SSAS_AWS_CLOUDWATCH_ALARM, t_ssas_aws_cloudwatch_alarm_records)

    oracle.delete_table(session, T_SSAS_AWS_CLOUDWATCH_LOG, account_id)
    oracle.insert_table(session, T_SSAS_AWS_CLOUDWATCH_LOG, t_ssas_aws_cloudwatch_logs_records)

    return 0