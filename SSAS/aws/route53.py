from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_ROUTE53 import T_SSAS_AWS_ROUTE53


def execute(account_id, session, **credential_key):

    route53_client = clients.get_client_by_key('route53', **credential_key)

    t_ssas_aws_route53_records = []
    hosted_zones = []
    next_marker = None
    while True:
        if next_marker:
            response = route53_client.list_hosted_zones(Marker=next_marker)
        else:
            response = route53_client.list_hosted_zones()

        hosted_zones.extend(response.get('HostedZones', []))
        if response.get('IsTruncated'):
            next_marker = response.get('NextMarker')
        else:
            break

    for zone in hosted_zones:
        t_ssas_aws_route53 = T_SSAS_AWS_ROUTE53()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_route53.account_id = account_id
        t_ssas_aws_route53.host_zone_id = zone.get('Id')
        t_ssas_aws_route53.host_zone_name = zone.get('Name')
        t_ssas_aws_route53.create_time = current_datetime
        t_ssas_aws_route53_records.append(t_ssas_aws_route53)

    oracle.delete_table(session, T_SSAS_AWS_ROUTE53, account_id)
    oracle.insert_table(session, T_SSAS_AWS_ROUTE53, t_ssas_aws_route53_records)

    return 0