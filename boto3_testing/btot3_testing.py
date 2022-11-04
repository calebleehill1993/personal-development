__author__ = 'chill'

import os
import sys
from datetime import datetime, date, timedelta
from tools.sql_templating.sql_executor import TemplateExecutor
from tools.qa_job_log import qa_job_decorator
from tools import this_dir
import boto3
from tools.aws_config import get_aws_key

executor = TemplateExecutor(verbose_log_file='sys.stdout',
                            execute_flag=True,
                            base_dir=this_dir(__file__),
                            silent=False)

# sends given file to s3 with the given key
def to_s3(file_path, key):
    # send edited file to s3
    print("connect to s3")
    bucket_name = 'adhoctemp'
    s3_client = boto3.client('s3',
                             aws_access_key_id=get_aws_key('devadmin')['aws_access_key_id'],
                             aws_secret_access_key=get_aws_key('devadmin')['aws_secret_access_key'])
    # The file_path is the local path to the file to upload
    # The bucket_name is where is S3 we want to put the file
    # The key is the name of the file
    s3_client.upload_file(file_path, bucket_name, key)


# copies from s3 into redshift. insert boolean is for if the table should be truncated first or if the copy
# should keep the old data.
def to_redshift(table_name, key, insert):
    # The code from here on was done in redshift but can be done here as well. This is copying
    # the gzip from s3 over to redshift.
    print("call from s3 through redshift")
    if insert is False:
        truncate = """
        truncate {table_name}
        """.format(table_name=table_name)
        executor.execute(truncate)
    sql_copy = """
    copy {table_name}
    from 's3://adhoctemp/{key}'
    IAM_ROLE 'arn:aws:iam::719465667078:role/Redshift-Load-Unload'
    dateformat 'auto'
    acceptinvchars
    CSV
    TRUNCATECOLUMNS
    IGNOREHEADER 1;
     """.format(table_name=table_name, key=key)
    executor.execute(sql_copy)

file_dir = os.path.join(os.getcwd(), 'Namely Report - Data Science Report.csv')
namely_key = 'namely_data'
namely_table = 'test.tbl_namely'

to_s3(file_dir, namely_key)
to_redshift(namely_table, namely_key, False)
