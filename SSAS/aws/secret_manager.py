from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_SECRET import T_SSAS_AWS_SECRET
import json
import re


def mask_passwords(secret_string):
    secret_data = json.loads(secret_string)
    password_patterns = [
        re.compile(r'password', re.IGNORECASE),
        re.compile(r'secret', re.IGNORECASE),
        re.compile(r'secret_access_key', re.IGNORECASE),
        re.compile(r's3_secret', re.IGNORECASE),
        re.compile(r'app_secret', re.IGNORECASE),
        re.compile(r'SecretKey', re.IGNORECASE)
    ]
    for key, value in secret_data.items():
        if any(pattern.search(key) for pattern in password_patterns):
            secret_data[key] = 'XXXXXX'
    return json.dumps(secret_data)


def get_secret(client, secret_name):

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    return get_secret_value_response['SecretString']


def execute(account_id, session, **credential_key):

    secrets_manager_client = clients.get_client_by_key('secretsmanager', **credential_key)

    t_ssas_aws_secret_records = []
    secrets = []
    next_token = None

    while True:
        if next_token:
            response = secrets_manager_client.list_secrets(NextToken=next_token)
        else:
            response = secrets_manager_client.list_secrets()

        secrets.extend(response.get('SecretList', []))
        next_token = response.get('NextToken')

        if not next_token:
            break

    for secret in secrets:
        t_ssas_aws_secret = T_SSAS_AWS_SECRET()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_secret.account_id = account_id
        t_ssas_aws_secret.secret_name = secret.get('Name')
        print(secret.get('Name'))

        ignore_flg = 'N'
        secrets_ignore = ["airflowfdna", "github/pat", "ansible/token", 'ADuser/pass', 'qliksns-qwkey-secret']
        for secret_ignore in secrets_ignore:
            if secret_ignore in secret.get('Name'):
                t_ssas_aws_secret.secret_value = ''
                ignore_flg = 'Y'
                break

        if ignore_flg == 'N':
            secret_string = get_secret(secrets_manager_client, secret.get('Name'))
            t_ssas_aws_secret.secret_value = mask_passwords(secret_string)

        t_ssas_aws_secret.create_time = current_datetime
        t_ssas_aws_secret_records.append(t_ssas_aws_secret)

    oracle.delete_table(session, T_SSAS_AWS_SECRET, account_id)
    oracle.insert_table(session, T_SSAS_AWS_SECRET, t_ssas_aws_secret_records)

    return 0