from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_KMS import T_SSAS_AWS_KMS


def execute(account_id, session, **credential_key):

    kms_client = clients.get_client_by_key('kms', **credential_key)

    t_ssas_aws_kms_records = []

    aliases = []
    next_marker = None
    truncated = True

    while truncated:
        if next_marker:
            response = kms_client.list_aliases(Marker=next_marker)
        else:
            response = kms_client.list_aliases()

        aliases.extend(response.get('Aliases', []))
        next_marker = response.get('NextMarker')
        truncated = response.get('Truncated', False)

    keys = []
    next_marker = None
    truncated = True

    while truncated:
        if next_marker:
            response = kms_client.list_keys(Marker=next_marker)
        else:
            response = kms_client.list_keys()

        keys.extend(response.get('Keys', []))
        aliases.extend(response.get('Aliases', []))
        next_marker = response.get('NextMarker')
        truncated = response.get('Truncated', False)

    for key in keys:
        t_ssas_aws_kms = T_SSAS_AWS_KMS()
        current_datetime = datetime.datetime.now()

        key_id = key.get('KeyId')
        key_info = kms_client.describe_key(KeyId=key_id)
        key_metadata = key_info.get('KeyMetadata', {})

        t_ssas_aws_kms.account_id = account_id
        for alias in aliases:
            if alias.get('TargetKeyId') == key_metadata.get('KeyId'):
                t_ssas_aws_kms.key_alias = alias.get('AliasName')
                break
        t_ssas_aws_kms.key_id = key_metadata.get('KeyId')
        t_ssas_aws_kms.key_manager = key_metadata.get('KeyManager')
        t_ssas_aws_kms.key_status = key_metadata.get('KeyState')
        t_ssas_aws_kms.create_time = current_datetime
        t_ssas_aws_kms_records.append(t_ssas_aws_kms)

    oracle.delete_table(session, T_SSAS_AWS_KMS, account_id)
    oracle.insert_table(session, T_SSAS_AWS_KMS, t_ssas_aws_kms_records)

    return 0