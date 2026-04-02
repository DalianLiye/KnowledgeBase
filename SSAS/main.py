from aws import acm, cloudwatch, dynamodb, security_group, ec2, efs, glue, iam, kms, lambda_function, rds, redshift, \
    resource_group, route53_resolver, route53, s3, secret_manager, sns, sqs, ssm, sts, vpc, step_functions
from common.connection.aws import clients
from common.connection.db import oracle
import json


if __name__ == '__main__':
    env = 'all'  # dev, tst, uat, prd, all

    if env == 'all':
        envs = ['dev', 'tst', 'uat', 'prd']
    else:
        envs = [env]

    for env in envs:
        secret_id = f"/CXXXX/XXXXX/{env}"

        secrets_manager_client = clients.get_client_by_profile('iac_cn_dev', 'secretsmanager')

        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=secret_id
        )

        credential_key = json.loads(get_secret_value_response['SecretString'])

        sts_client = clients.get_client_by_key('sts', **credential_key)
        response = sts_client.get_caller_identity()
        account_id = response['Account']

        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId='/hhiecn/ssas/oracle'
        )

        oracle_con_info = json.loads(get_secret_value_response['SecretString'])

        hostname = oracle_con_info['hostname']
        port = oracle_con_info['port']
        service_name = oracle_con_info['service_name']
        username = oracle_con_info['username']
        password = oracle_con_info['password']

        engine = oracle.create_engine_ora(**oracle_con_info)
        session = oracle.create_session(engine)

        result = glue.execute(account_id, session, **credential_key)
        print("glue信息已成功导入DB。")




        '''
        result = acm.execute(account_id, session, **credential_key)
        print("acm信息已成功导入DB。")

        result = redshift.execute(account_id, session, **credential_key)
        print("redshift信息已成功导入DB。")

        result = resource_group.execute(account_id, session, **credential_key)
        print("resource_group信息已成功导入DB。")

        result = route53_resolver.execute(account_id, session, **credential_key)
        print("route53_resolver信息已成功导入DB。")

        result = ssm.execute(account_id, session, **credential_key)
        print("ssm信息已成功导入DB。")

        result = step_functions.execute(account_id, session, **credential_key)
        print("step_functions信息已成功导入DB。")

        result = security_group.execute(account_id, session, **credential_key)
        print("security group信息已成功导入DB。")

        result = efs.execute(account_id, session, **credential_key)
        print("efs信息已成功导入DB。")

        result = secret_manager.execute(account_id, session, **credential_key)
        print("secret_manager信息已成功导入DB。")

        result = sts.execute(env, session, **credential_key)
        print("account信息已成功导入DB。")

        result = cloudwatch.execute(account_id, session, **credential_key)
        print("cloudwatch信息已成功导入DB。")

        result = route53.execute(account_id, session, **credential_key)
        print("route53信息已成功导入DB。")

        result = kms.execute(account_id, session, **credential_key)
        print("kms信息已成功导入DB。")

        result = sns.execute(account_id, session, **credential_key)
        print("sns信息已成功导入DB。")

        result = sqs.execute(account_id, session, **credential_key)
        print("sqs信息已成功导入DB。")

        result = dynamodb.execute(account_id, session, **credential_key)
        print("dynamodb信息已成功导入DB。")

        result = glue.execute(account_id, session, **credential_key)
        print("glue信息已成功导入DB。")

        result = ec2.execute(account_id, session, **credential_key)
        print("ec2信息已成功导入DB。")

        result = s3.execute(account_id, session, **credential_key)
        print("S3 bucket信息已成功导入DB。")

        result = vpc.execute(account_id, session, **credential_key)
        print("vpc信息已成功导入DB。")

        result = rds.execute(account_id, session, **credential_key)
        print("rds信息已成功导入DB。")

        result = lambda_function.execute(account_id, session, **credential_key)
        print("lambda信息已成功导入DB。")

        result = iam.execute(account_id, session, **credential_key)
        print("IAM信息已成功导入DB。")
        '''
        session.close()