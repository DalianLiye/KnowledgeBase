from common.connection.aws import clients
from common.connection.db import oracle
import datetime
from common.model.T_SSAS_AWS_ACM_CERTIFICATE import T_SSAS_AWS_ACM_CERTIFICATE


def execute(account_id, session, **credential_key):

    acm_client = clients.get_client_by_key('acm', **credential_key)

    t_ssas_aws_acm_certificate_records = []
    certificates = []
    next_token = None

    while True:
        if next_token:
            response = acm_client.list_certificates(NextToken=next_token)
        else:
            response = acm_client.list_certificates()

        certificates.extend(response.get('CertificateSummaryList', []))
        next_token = response.get('NextToken')

        if not next_token:
            break

    for cert in certificates:
        t_ssas_aws_acm_certificate = T_SSAS_AWS_ACM_CERTIFICATE()
        current_datetime = datetime.datetime.now()
        cert_arn = cert['CertificateArn']

        cert_details = acm_client.describe_certificate(CertificateArn=cert_arn)
        certificate = cert_details['Certificate']

        t_ssas_aws_acm_certificate.account_id = account_id
        t_ssas_aws_acm_certificate.certificate_id = cert_arn.split('/')[-1]
        t_ssas_aws_acm_certificate.domain_name = certificate.get('DomainName')
        t_ssas_aws_acm_certificate.certificate_type = certificate.get('Type')
        t_ssas_aws_acm_certificate.certificate_status = certificate.get('Status')
        in_use_by = certificate.get('InUseBy', [])
        if in_use_by:
            t_ssas_aws_acm_certificate.is_in_use = 'yes'

        t_ssas_aws_acm_certificate.create_time = current_datetime
        t_ssas_aws_acm_certificate_records.append(t_ssas_aws_acm_certificate)

    oracle.delete_table(session, T_SSAS_AWS_ACM_CERTIFICATE, account_id)
    oracle.insert_table(session, T_SSAS_AWS_ACM_CERTIFICATE, t_ssas_aws_acm_certificate_records)

    return 0