import os
import sys
sys.path.insert(0, '/Users/calebhill/Documents/ds-datascience/_playground')
print(os.getcwd())
from email_with_python.email_with_python import send_message

import random

import pandas as pd
from matplotlib import pyplot as plt

pickle_path = os.path.join(os.path.dirname(__file__), 'low_fares_over_time.pkl')

df = pd.read_pickle(pickle_path)

linestyles = ['solid', 'dotted', 'dashed']

for date_range in df['date_range']:
    latest_run = df.loc[(df['date_range'] == date_range) & (df['extract_date'] == df['extract_date'].max()), 'total_cost'].iloc[0]
    plt.plot(df.loc[df['date_range'] == date_range, 'extract_date'],
             df.loc[df['date_range'] == date_range, 'total_cost'],
             label=f'{date_range} - ${latest_run}', linestyle=random.choice(linestyles))

# plt.legend()
plt.savefig('southwest_report.png')

send_message('calebleehill1993@gmail.com', 'Test Message', '<p>This is a test</p>', ['southwest_report.png'])
os.remove('southwest_report.png')
