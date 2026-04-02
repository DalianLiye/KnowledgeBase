from common.connection.aws import clients
from common.connection.db import oracle
from common.model.T_SSAS_AWS_GLUE import T_SSAS_AWS_GLUE
import datetime


def execute(account_id, session, **credential_key):
    glue_client = clients.get_client_by_key('glue', **credential_key)
    t_ssas_aws_glue_records = []

    jobs = []
    next_token = None

    while True:
        if next_token:
            response = glue_client.get_jobs(NextToken=next_token)
        else:
            response = glue_client.get_jobs()

        jobs.extend(response.get('Jobs', []))
        next_token = response.get('NextToken')

        if not next_token:
            break

    for job in jobs:

        t_ssas_aws_glue = T_SSAS_AWS_GLUE()
        current_datetime = datetime.datetime.now()

        t_ssas_aws_glue.account_id = account_id

        t_ssas_aws_glue.glue_name = job['Name']
        t_ssas_aws_glue.glue_description = job.get('Description', 'Unknown')
        t_ssas_aws_glue.glue_role = job.get('Role', 'Unknown')

        t_ssas_aws_glue.glue_type = job['Command'].get('Name', 'Unknown')
        t_ssas_aws_glue.glue_scriptlocation = job['Command'].get('ScriptLocation', 'Unknown')
        t_ssas_aws_glue.glue_pythonversion = str(job['Command'].get('PythonVersion', 'Unknown'))
        t_ssas_aws_glue.glue_dataprocessunit = str(job.get('MaxCapacity', 'Unknown'))
        t_ssas_aws_glue.glue_timeout = str(job.get('Timeout', 'Unknown'))
        t_ssas_aws_glue.glue_maxretries = str(job.get('MaxRetries', 'Unknown'))
        t_ssas_aws_glue.glue_jobmode = job.get('JobMode', 'Unknown')

        if job.get('CreatedOn', None) is None:
            t_ssas_aws_glue.glue_createdon = 'Unknown'
        else:
            t_ssas_aws_glue.glue_createdon = job['CreatedOn'].strftime('%Y-%m-%d %H:%M:%S.%f')

        if job.get('LastModifiedOn', None) is None:
            t_ssas_aws_glue.glue_lastmodifiedon = 'Unknown'
        else:
            t_ssas_aws_glue.glue_lastmodifiedon = job['LastModifiedOn'].strftime('%Y-%m-%d %H:%M:%S.%f')

        if job.get('Connections', None) is None:
            t_ssas_aws_glue.glue_connections = 'Unknown'
        else:
            t_ssas_aws_glue.glue_connections = str(job['Connections'].get('Connections','Unknown'))

        if job.get('DefaultArguments', None) is None:
            t_ssas_aws_glue.glue_defaultarguments = 'Unknown'
        else:
            t_ssas_aws_glue.glue_defaultarguments = str(job['DefaultArguments'])

        if job.get('ExecutionProperty', None) is None:
            t_ssas_aws_glue.glue_maxconcurrentruns = 'Unknown'
        else:
            t_ssas_aws_glue.glue_maxconcurrentruns = job['ExecutionProperty'].get('MaxConcurrentRuns', 'Unknown')

        t_ssas_aws_glue.glue_version = job.get('GlueVersion', 'Unknown')
        t_ssas_aws_glue.create_time = current_datetime

        t_ssas_aws_glue_records.append(t_ssas_aws_glue)

    oracle.delete_table(session, T_SSAS_AWS_GLUE, account_id)
    oracle.insert_table(session, T_SSAS_AWS_GLUE, t_ssas_aws_glue_records)

    return 0