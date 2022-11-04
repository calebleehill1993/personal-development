__author__ = 'chill'

import logging
import os
import sys
from pprint import pprint

from tools.sql_templating.sql_executor import TemplateExecutor
from tools import this_dir
from tools.qa_job_log import qa_job_decorator
import pandas as pd
from datetime import date

# Setting to display all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)

pd.set_option('display.max_rows', 100)

# -----------------------------------------------------------------------------------
#   Title:f
#   Purpose:
#   Created:
#   Modifications:
# -----------------------------------------------------------------------------------

JOB_NAME = 'Job Name'

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
ch.setLevel(logging.WARNING)
ch.setFormatter(logFormatter)

# Create file handler, set level and apply format
fh = logging.FileHandler(os.path.join(LOG_PATH, LOG_FILE), 'w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logFormatter)

# Add handlers to logger
log.addHandler(ch)
log.addHandler(fh)

executor = TemplateExecutor(verbose_log_file=log,
                            execute_flag=True,
                            base_dir=this_dir(__file__),
                            silent=False)

# @qa_job_decorator(job_id=xx, job_name=JOB_NAME)  # TODO: Enter Job ID
def wrapper_function():
    query = """ SELECT report_guid,
                       job_title,
                       departments,
                       departure_date,
                       start_date,
                       employee_type,
                       office_locations,
                       employee_name,
                       reports_to_name,
                       country_name,
                       extract_date
                FROM namely.namely_report
                WHERE extract_date >= '2022-09-01'"""
    # executor.execute(sql='path_to_file', params=dict())
    data = executor.execute(sql=query, params=dict())

    columns = ['report_guid',
       'job_title',
       'departments',
       'departure_date',
       'start_date',
       'employee_type',
       'office_locations',
       'employee_name',
       'reports_to_name',
       'country_name',
       'extract_date']

    df = pd.DataFrame.from_records(data, columns=columns)

    charles = {'report_guid': ['7b974fae-a6fc-45a3-a933-305b2eba1d7d'],
     'job_title': ['CEO'],
     'departments': ['Executive'],
     'departure_date': [None],
     'start_date': [date(2010, 1, 1)],
     'employee_type': ['Full Time'],
     'office_locations': ['Company HQ'],
     'employee_name': ['Charles Manning'],
     'reports_to_name': [''],
     'country_name': ['United States']}

    charles_df = pd.DataFrame(charles, columns=columns)

    # Adding Charles
    exit_loop = False
    for j in range(9, 11):
        if exit_loop:
            break
        for i in range(1, 31):
            if j == 10 and i == 19:
                exit_loop = True
                break
            charles_df['extract_date'] = date(2022, 9, i)
            df = pd.concat([df, charles_df], ignore_index=True)

    df['level'] = None
    df['full_reports_to'] = ''
    # df['full_reports_to'] = df['full_reports_to'].astype('object')
    #
    # for i in range(len(df)):
    #     df.at[i, 'full_reports_to'] = [].copy()

    conditions = (df['departure_date'].isnull()) \
                 & (df['reports_to_name'] == '') \
                 & (df['start_date'] <= date.today()) \
                 & (df['employee_name'] != 'Time Off Admin')

    df.loc[conditions, 'level'] = 1

    # Assigning levels under Charles Manning
    for i in range(2, 10):
        conditions = (df['reports_to_name'].isin(list(df.loc[(df['level'] == i - 1), 'employee_name'])))\
                     & (df['start_date'] <= date.today()) \
                     & (df['employee_name'] != 'Time Off Admin')
        df.loc[conditions, 'level'] = i
        print(df.loc[conditions, :])

    #print(df.dtypes)

    df.sort_values(by = ['extract_date', 'level'], inplace=True, ignore_index=True)

    for i in range(len(df)):
        if df.at[i, 'reports_to_name'] != '':
            try:
                full_report = df.loc[(df['employee_name'] == df.at[i, 'reports_to_name']) & (df['extract_date'] == df.at[i, 'extract_date']), 'full_reports_to'].iloc[0]
            # Catches if nothing matches
            except IndexError:
                continue
            if df.at[i, 'level'] is not None and df.at[i, 'level'] > 2:
                full_report += ','
            full_report += df.at[i, 'reports_to_name']
            df.at[i, 'full_reports_to'] = full_report

    #print(df.iloc[100:120])

    #print(df.loc[(df['full_reports_to'].str.contains('Bryce Kliewer')) & (df['departure_date'].isnull())])
    #print(len(df.loc[(df['full_reports_to'].str.contains('Bryce Kliewer')) & (df['departure_date'].isnull())]))


    # How do we connect the people who have departed and whose supervisor has also departed?
    # Associate by department
    # If department doesn't exist, have an other category.
    for index, row in df.loc[(df['full_reports_to'] == '') & (df['departments'] != '')].iterrows():
        lowest_level_in_department = df.loc[(df['extract_date'] == row['extract_date']) & (df['departments'] == row['departments']) & (df['departure_date'].isnull()), 'level'].min()
        lowest_level_person = df.loc[(df['extract_date'] == row['extract_date']) & (df['departments'] == row['departments']) & (df['level'] == lowest_level_in_department) & (df['departure_date'].isnull()), ['reports_to_name', 'employee_name']]

        # If there are more than 1 lowest level people, get the next lowest level person
        try:
            if len(lowest_level_person) > 1:
                lowest_level_person = lowest_level_person['reports_to_name'].iloc[0]
            else:
                lowest_level_person = lowest_level_person['employee_name'].iloc[0]
            df.at[index, 'reports_to_name'] = lowest_level_person
            full_report = df.loc[df['employee_name'] == lowest_level_person, 'full_reports_to'].iloc[0]
            if lowest_level_person != 'Charles Manning':
                full_report += ','
            full_report += lowest_level_person
            df.at[index, 'full_reports_to'] = full_report
        except IndexError:
            continue

    #print(df.loc[df['full_reports_to'] == ''])

    df['current_over'] = 0
    df['departed_over'] = 0
    df['current_over_total'] = 0
    df['departed_over_total'] = 0

    for i in range(len(df)):
        df.at[i, 'current_over'] = len(df.loc[(df['reports_to_name'] == df.at[i, 'employee_name']) & (df['extract_date'] == row['extract_date']) & (df['departure_date'].isnull())])
        df.at[i, 'departed_over'] = len(df.loc[(df['reports_to_name'] == df.at[i, 'employee_name']) & (df['extract_date'] == row['extract_date']) & (df['departure_date'].notnull())])
        df.at[i, 'current_over_total'] = len(df.loc[(df['full_reports_to'].str.contains(df.at[i, 'employee_name'])) & (df['extract_date'] == row['extract_date']) & (df['departure_date'].isnull())])
        df.at[i, 'departed_over_total'] = len(df.loc[(df['full_reports_to'].str.contains(df.at[i, 'employee_name'])) & (df['extract_date'] == row['extract_date']) & (df['departure_date'].notnull())])

    #print(df.head(20))

    #print(df.loc[df['employee_name'] == 'Vivian Watt'])

    df.to_csv('Namely Report.csv', index=False)

if __name__ == '__main__':
    wrapper_function()
