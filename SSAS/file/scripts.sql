drop table ssas_aws_s3;
create table ssas_aws_s3 (
	account_id varchar2(100),
	bucket_name varchar2(100),
	bucket_creation_date timestamp,
	bucket_description varchar2(1000),
	create_time timestamp
);

drop table ssas_aws_ec2;
create table ssas_aws_ec2 (
	account_id varchar2(100),
	ec2_instance_id varchar2(100),
	ec2_instance_name varchar2(100),
	ec2_instance_state varchar2(100),
	ec2_instance_type varchar2(100),
	ec2_instance_platform  varchar2(100),
	create_time timestamp
);

drop table ssas_aws_vpc;
create table ssas_aws_vpc (
	account_id varchar2(100),
	vpc_id varchar2(100),
	vpc_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_vpc_subnet;
create table ssas_aws_vpc_subnet (
	account_id varchar2(100),
	vpc_id varchar2(100),
	subnet_id varchar2(100),
	subnet_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_rds;
create table ssas_aws_rds (
	account_id varchar2(100),
	db_identifier varchar2(100),
	db_class varchar2(100),
	db_engine varchar2(100),
	db_engine_version varchar2(100),
	db_state varchar2(100),
	create_time timestamp
);

drop table ssas_aws_iam_user;
create table ssas_aws_iam_user (
	account_id varchar2(100),
	iam_user_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_iam_role;
create table ssas_aws_iam_role (
	account_id varchar2(100),
	iam_role_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_glue;
create table ssas_aws_glue (
	account_id varchar2(100),
	glue_name varchar2(100),
	glue_description varchar2(1000),
	glue_role varchar2(100),
	glue_type varchar2(100),
	glue_scriptlocation varchar2(1000),
	glue_pythonversion varchar2(100),
	glue_dataprocessunit varchar2(100),
	glue_timeout varchar2(100),
	glue_maxretries varchar2(100),
	glue_jobmode varchar2(100),
	glue_createdon varchar2(100),
	glue_lastmodifiedon varchar2(100),
	glue_connections varchar2(1000),
	glue_defaultarguments varchar2(4000),
	glue_maxconcurrentruns varchar2(1000),
	glue_version varchar2(100),
	create_time timestamp
);

drop table ssas_aws_dynamodb;
create table ssas_aws_dynamodb (
	account_id varchar2(100),
	table_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_sqs;
create table ssas_aws_sqs (
	account_id varchar2(100),
	sqs_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_acm_certificate;
create table ssas_aws_acm_certificate (
	account_id varchar2(100),
	certificate_id varchar2(100),
	domain_name varchar2(100),
	certificate_type varchar2(100),
	certificate_status varchar2(100),
	is_in_use varchar2(100),
	create_time timestamp
);

drop table ssas_aws_secret;
create table ssas_aws_secret (
	account_id varchar2(100),
	secret_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_redshift;
create table ssas_aws_redshift (
	account_id varchar2(100),
	cluster_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_kms;
create table ssas_aws_kms (
	account_id varchar2(100),
	key_alias varchar2(100),
	key_id varchar2(100),
	key_manager varchar2(100),
	key_status varchar2(100),
	create_time timestamp
);

drop table ssas_aws_route53;
create table ssas_aws_route53 (
	account_id varchar2(100),
	host_zone_id varchar2(100),
	host_zone_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_cloudwatch_alarm;
create table ssas_aws_cloudwatch_alarm (
	account_id varchar2(100),
	alarm_name varchar2(500),
	alarm_state varchar2(100),
	alarm_condition varchar2(2000),
	alarm_action varchar2(500),
	create_time timestamp
);

drop table ssas_aws_cloudwatch_log;
create table ssas_aws_cloudwatch_log(
	account_id varchar2(100),
	log_group_name varchar2(500),
	log_class varchar2(100),
	retention varchar2(2000),
	create_time timestamp
);

drop table ssas_aws_account;
create table ssas_aws_account (
	env varchar2(100),
	account_id varchar2(100),
	account_name varchar2(100),
	create_time timestamp
);

drop table ssas_aws_sns;
create table ssas_aws_sns
   (	account_id varchar2(100),
	topic_name varchar2(100),
	create_time timestamp (6)
   )

drop table ssas_aws_lambda;
create table ssas_aws_lambda
(	account_id varchar2(100),
	lambda_name varchar2(100),
	create_time timestamp (6)
)

drop table ssas_aws_efs;
create table ssas_aws_efs (
	account_id varchar2(100),
	efs_name varchar2(100),
	file_system_id varchar2(100),
	encrypted varchar2(100),
	total_size varchar2(100),
	Performance_mode varchar2(100),
	Throughput_mode varchar2(100),
	Automatic_backups varchar2(100),
	create_time timestamp
);


drop table ssas_aws_ec2_sg;
create table ssas_aws_ec2_sg (
	account_id varchar2(100),
	vpc_id varchar2(100),
	security_group_id varchar2(100),
	security_group_name varchar2(500),
	security_group_description varchar2(2000),
	create_time timestamp
);

drop table ssas_aws_stepfunction;
create table ssas_aws_stepfunction (
	account_id varchar2(100),
	state_machine_name varchar2(100),
	state_machine_type varchar2(100),
	state_machine_status varchar2(500),
	create_time timestamp
);


drop table ssas_aws_ssm_param;
create table ssas_aws_ssm_param (
	account_id varchar2(100),
	param_name varchar2(100),
	param_tier varchar2(100),
	param_type varchar2(100),
	create_time timestamp
);

drop table SSAS_AWS_ROUTE53_RESOLVER_ENDPOINT;
create table SSAS_AWS_ROUTE53_RESOLVER_ENDPOINT (
	account_id varchar2(100),
	endpoint_type varchar2(100),
	endpoint_id varchar2(100),
	endpoint_name varchar2(100),
	endpoint_status varchar2(100),
	host_vpc varchar2(100),
	create_time timestamp
);

drop table SSAS_AWS_REDSHIFT_SUBNET_GROUP;
create table SSAS_AWS_REDSHIFT_SUBNET_GROUP (
	account_id varchar2(100),
	subnet_group_name varchar2(100),
	subnet_group_status varchar2(100),
	vpc_id varchar2(100),
	create_time timestamp
);

drop table SSAS_AWS_REDSHIFT_PARAM_GROUP;
create table SSAS_AWS_REDSHIFT_PARAM_GROUP (
	account_id varchar2(100),
	param_group_name varchar2(100),
	create_time timestamp
);

drop table SSAS_AWS_REDSHIFT_PARAM_GROUP;
create table SSAS_AWS_REDSHIFT_PARAM_GROUP (
	account_id varchar2(100),
	param_group_name varchar2(100),
	create_time timestamp
);