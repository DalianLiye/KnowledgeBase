import boto3

def get_client_by_profile(profile_name, client_name):
    session = boto3.Session(profile_name=profile_name)
    client = session.client(client_name)
    return client


def get_client_by_key(client_name, **credential_key):
    client = boto3.client(client_name, **credential_key)
    return client


def get_client_by_default(service_name, region_name):
    session = boto3.session.Session()
    client = session.client(
        service_name=service_name,
        region_name=region_name
    )
    return client