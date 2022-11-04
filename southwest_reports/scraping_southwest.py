# Southwest could detect that I was using Selenium so I had to get around that by changing the $cdc_ variable in the
# chromedriver to $dog_ using vim.
# vim /path/to/chromedriver
# Replace all instances of cdc_ with dog_ by typing :%s/cdc_/dog_/g
# :wq!    this saves the file
# https://technoteshelp.com/javascript-can-a-website-detect-when-you-are-using-selenium-with-chromedriver/


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# Used for scrapping websites from HTML
from bs4 import BeautifulSoup
import os
import pandas as pd
import time
from datetime import date

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")


# Southwest
browser = webdriver.Chrome(options=options)

browser.get('https://www.southwest.com/air/low-fare-calendar')
time.sleep(5)
assert 'Southwest' in browser.title

elem = browser.find_element(By.ID, 'originationAirportCode')
elem.clear()
elem.__setattr__('value', 'Spokane, WA - GEG')
time.sleep(.5)
elem.send_keys(Keys.RETURN)
elem = browser.find_element(By.ID, 'destinationAirportCode')
elem.clear()
elem.send_keys('Dallas (Love Field), TX - DAL')
time.sleep(.5)
elem.send_keys(Keys.RETURN)
elem = browser.find_element(By.ID, 'departureDate')
elem.send_keys('December 2022')
time.sleep(.5)
elem.send_keys(Keys.RETURN)
elem = browser.find_element(By.ID, 'form-mixin--submit-button')
time.sleep(1)
elem.click()
time.sleep(5)

html_path = os.path.join(os.path.dirname(__file__), 'southwest_index.html')

with open(html_path, "w") as f:
    f.write(browser.page_source)

today = date.today()
costs = []

with open(html_path, "r") as f:
    soup = BeautifulSoup(f, 'html.parser')

    sections = soup.find_all("div", {"class": "air-low-fare-calendar-matrix-secondary"})
    buttons = sections[0].find_all("div", {"class": "air-low-fare-calendar-date-mismatch-flyout"})

    flight_type = 'departure'

    for i in range(2):
        buttons = sections[i].find_all("div", {"class": "air-low-fare-calendar-date-mismatch-flyout"})
        if i == 1:
            flight_type = 'return'
        for button in buttons:
            if button.find("div", {"class": "content-cell--day"}).text:
                d = date(2022, 12, int(button.find("div", {"class": "content-cell--day"}).text))
                day_of_week = d.strftime('%a')
                cost = (flight_type, d, day_of_week, int(button.find("span", {"class": "content-cell--fare_usd"}).text))
                costs.append(cost)

os.remove(html_path)

columns = ['flight_direction', 'date', 'day_of_week', 'cost']

df = pd.DataFrame(costs, columns=columns)
df['date'] = pd.to_datetime(df['date'])

# Gets how far we are from Christmas
df['days_from_christmas'] = df['date'].dt.day - 25

possible_departures = df.loc[(-7 <= df.days_from_christmas) & (df.days_from_christmas <= -2) & (df.flight_direction == 'departure')]
possible_returns = df.loc[(1 <= df.days_from_christmas) & (df.days_from_christmas <= 7) & (df.flight_direction == 'return')]

combos = pd.merge(possible_departures, possible_returns, how='cross')

combos['stay_length'] = combos['days_from_christmas_y'] - combos['days_from_christmas_x']

combos = combos.loc[(7 <= combos['stay_length']) & (combos['stay_length'] <= 11),
                 ['day_of_week_x', 'date_x', 'cost_x', 'day_of_week_y', 'date_y',
                  'cost_y', 'stay_length']].sort_values(['date_x', 'date_y'], ascending=[True, True])

combos['total_cost'] = combos['cost_x'] + combos['cost_y']

combos['date_range'] = combos['day_of_week_x'] + ' ' + combos['date_x'].dt.day.astype(str) +\
                       ' to ' + combos['day_of_week_y'] + ' ' + combos['date_y'].dt.day.astype(str)

combos.drop(['day_of_week_x', 'day_of_week_y', 'date_x', 'date_y'], axis=1, inplace=True)

combos.rename(columns={'cost_x': 'dep_cost', 'cost_y': 'ret_cost'}, inplace=True)

combos['extract_date'] = today

combos = combos[['extract_date', 'date_range', 'stay_length', 'dep_cost', 'ret_cost', 'total_cost']].reset_index(drop=True)

csv_path = os.path.join(os.path.dirname(__file__), today.strftime('%Y-%m-%d') + '_low_fares.csv')

combos.to_csv(csv_path, index=False)

pickle_path = os.path.join(os.path.dirname(__file__), 'low_fares_over_time.pkl')

all_time = pd.read_pickle(pickle_path)

all_time = all_time[all_time['extract_date'] != today]

all_time = pd.concat([all_time, combos]).reset_index(drop=True)

all_time.to_pickle(pickle_path)

lowest_path = os.path.join(os.path.dirname(__file__), 'lowest_fare_over_time.csv')

all_time.groupby(by='extract_date').min('total_cost').to_csv(lowest_path)

