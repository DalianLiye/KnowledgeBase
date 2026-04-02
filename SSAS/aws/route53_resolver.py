from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_ROUTE53_RESOLVER_ENDPOINT import T_SSAS_AWS_ROUTE53_RESOLVER_ENDPOINT


def execute(account_id, session, **credential_key):

    route53resolver_client = clients.get_client_by_key('route53resolver', **credential_key)

    t_ssas_aws_route53_resolver_endpoint_records = []

    paginator = route53resolver_client.get_paginator('list_resolver_endpoints')

    for page in paginator.paginate():
        for endpoint in page['ResolverEndpoints']:
            t_ssas_aws_route53_resolver_endpoint = T_SSAS_AWS_ROUTE53_RESOLVER_ENDPOINT()
            current_datetime = datetime.datetime.now()

            t_ssas_aws_route53_resolver_endpoint.account_id = account_id
            t_ssas_aws_route53_resolver_endpoint.endpoint_type = endpoint['Direction']
            t_ssas_aws_route53_resolver_endpoint.endpoint_id = endpoint['Id']
            t_ssas_aws_route53_resolver_endpoint.endpoint_name = endpoint.get('Name', 'N/A')
            t_ssas_aws_route53_resolver_endpoint.endpoint_status = endpoint['Status']
            t_ssas_aws_route53_resolver_endpoint.host_vpc = endpoint['HostVPCId']
            t_ssas_aws_route53_resolver_endpoint.create_time = current_datetime
            t_ssas_aws_route53_resolver_endpoint_records.append(t_ssas_aws_route53_resolver_endpoint)

    oracle.delete_table(session, T_SSAS_AWS_ROUTE53_RESOLVER_ENDPOINT, account_id)
    oracle.insert_table(session, T_SSAS_AWS_ROUTE53_RESOLVER_ENDPOINT, t_ssas_aws_route53_resolver_endpoint_records)

    return 0