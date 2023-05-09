
from datetime import date, datetime
import time
from tools.qa_job_log import qa_job_decorator

from tools import this_dir
from tools.aws_config import get_aws_key
from tools.sql_templating.sql_executor import TemplateExecutor
import logging, os, sys

JOB_NAME = 'App SDK Partition Table'

# -----------------------------------------------------------------------------------
# Set up Logging

# File Path Config
LOG_PATH = os.path.join(this_dir(__file__), 'log')
if os.path.exists(LOG_PATH) is False:
    os.mkdir(LOG_PATH)
LOG_FILE = '{0}.log'.format(JOB_NAME.lower().replace(' ', '_'))

# Set up default logging level
log = logging.getLogger(JOB_NAME)
log.setLevel(logging.DEBUG)

# Set formatting
logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - Line:%(lineno)d - %(message)s')

# Create console handler, set level and apply format
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(logFormatter)

# Create file handler, set level and apply format
fh = logging.FileHandler(os.path.join(LOG_PATH, LOG_FILE), 'w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logFormatter)

# Add handlers to logger
log.addHandler(ch)
log.addHandler(fh)

executor = TemplateExecutor(default_params=dict(
    **get_aws_key('devadmin')),
    verbose_log_file=log,
    execute_flag=True,
    base_dir=this_dir(__file__),
    silent=False)


@qa_job_decorator(job_id=42,
                  job_name='App SDK Partition Table',
                  test_flag=False,
                  )
def wrapper():
    import redshift_connector
    conn = redshift_connector.connect(
        host='kochava-redshift-dev.c0gvx03xevos.us-west-2.redshift.amazonaws.com',
        database='dev',
        port=5439,
        user='devadmin',
        password='' # Look in 1Password for this
    )

    conn.autocommit = True

    # Create a Cursor object
    cursor = conn.cursor()

    start = date(2022, 2, 1)
    end = date(2023, 3, 1)
    current = start

    while current <= end:

        title_date = current.strftime('%Y%m')
        month = current.strftime('%Y-%m-%d')

        sql = f"""CREATE TABLE app_store_data.tbl_app_sdk_data_{title_date}
                    (
                        snapshot_date           DATE ENCODE AZ64,
                        ko_app_id               INTEGER ENCODE AZ64,
                        id                      INTEGER ENCODE AZ64,
                        package_code            VARCHAR(256) ENCODE ZSTD,
                        bundle_id               VARCHAR(256) ENCODE ZSTD,
                        store                   VARCHAR(20) ENCODE ZSTD,
                        name                    VARCHAR(256) ENCODE ZSTD,
                        description             VARCHAR(65535) ENCODE ZSTD,
                        category_id             INTEGER ENCODE AZ64,
                        subcategory_id          INTEGER ENCODE AZ64,
                        category_ids            VARCHAR(40) ENCODE ZSTD,
                        publisher_id            INTEGER ENCODE AZ64,
                        publisher_name          VARCHAR(1500) ENCODE ZSTD,
                        downloads               INTEGER ENCODE AZ64,
                        sdk_id                  INTEGER ENCODE AZ64,
                        sdk_active              BOOLEAN ENCODE ZSTD,
                        sdk_name                VARCHAR(100) ENCODE ZSTD,
                        sdk_company             VARCHAR(100) ENCODE ZSTD,
                        sdk_function            VARCHAR(25) ENCODE ZSTD,
                        category_name           VARCHAR(25) ENCODE ZSTD,
                        subcategory_name        VARCHAR(40) ENCODE ZSTD,
                        price_cents             INTEGER ENCODE AZ64,
                        offers_in_app_purchases BOOLEAN,
                        app_store_url           VARCHAR(1000) ENCODE ZSTD,
                        initial_release_date    DATE ENCODE AZ64,
                        current_version         VARCHAR(10000) ENCODE ZSTD,
                        last_update_date        DATE ENCODE AZ64,
                        icon_url                VARCHAR(300) ENCODE ZSTD,
                        screenshot_urls         VARCHAR(25000) ENCODE ZSTD,
                        app_permissions         VARCHAR(10000) ENCODE ZSTD,
                        privacy_url             VARCHAR(4096) ENCODE ZSTD,
                        downloads_revenue       DOUBLE PRECISION ENCODE ZSTD,
                        iap_revenue             DOUBLE PRECISION ENCODE ZSTD,
                        ad_revenue              DOUBLE PRECISION ENCODE ZSTD,
                        total_revenue           DOUBLE PRECISION ENCODE ZSTD,
                        daily_active_users      BIGINT ENCODE AZ64,
                        monthly_active_users    BIGINT ENCODE AZ64,
                        engagement              DOUBLE PRECISION ENCODE ZSTD,
                        sdk_present             BOOLEAN ENCODE ZSTD,
                        sdk_install_date        DATE ENCODE AZ64,
                        sdk_uninstall_date      DATE ENCODE AZ64,
                        sdk_activation_date     DATE ENCODE AZ64,
                        sdk_deactivation_date   DATE ENCODE AZ64
                    )
                        SORTKEY (snapshot_date);
        """.format(title_date=title_date)

        log.info(sql)

        cursor.execute(sql)

        sql = f"""INSERT INTO app_store_data.tbl_app_sdk_data_{title_date} (snapshot_date, ko_app_id, id, package_code, bundle_id, store, name, description,
                                     category_id, subcategory_id, category_ids, publisher_id, publisher_name, downloads,
                                     sdk_id, sdk_active, sdk_name, sdk_company, sdk_function, category_name,
                                     subcategory_name, price_cents, offers_in_app_purchases, app_store_url,
                                     initial_release_date, current_version, last_update_date, icon_url, screenshot_urls,
                                     app_permissions, privacy_url, downloads_revenue, iap_revenue, ad_revenue,
                                     total_revenue, daily_active_users, monthly_active_users, engagement, sdk_present,
                                     sdk_install_date, sdk_uninstall_date, sdk_activation_date, sdk_deactivation_date)
                    SELECT *
                    FROM app_store_data.tbl_app_sdk_data
                    WHERE DATE_TRUNC('month', snapshot_date) = '{month}';
        """.format(title_date=title_date, month=month)

        log.info(sql)

        cursor.execute(sql)

        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)

if __name__ == "__main__":
    wrapper()
