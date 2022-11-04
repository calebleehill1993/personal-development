# I had many issues trying to log into google with chrome so I switched to Firefox.
# Had to install a couple of things to run headless on the linux server
# https://azevedorafaela.com/tag/headless-browser-in-ubuntu/

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd
from datetime import date
from selenium import webdriver
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import sys

# Set up Logging

# File Path Config
LOG_PATH = os.path.join(os.path.dirname(__file__), 'log')
if os.path.exists(LOG_PATH) is False:
    os.mkdir(LOG_PATH)
LOG_FILE = '{0}.log'.format(__file__.lower().replace(' ', '_'))

# Set up default logging level
log = logging.getLogger(__file__)
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

geckodriver_autoinstaller.install()

# profile = webdriver.FirefoxProfile(
#     '/Users/calebhill/Library/Application Support/Firefox/Profiles/1nrpuadl.church_messenger')

profile = webdriver.FirefoxProfile(
    os.path.join(os.path.dirname(__file__), '1nrpuadl.church_messenger'))

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)

profile.set_preference("network.http.pipelining", True)
profile.set_preference("network.http.proxy.pipelining", True)
profile.set_preference("network.http.pipelining.maxrequests", 8)
profile.set_preference("content.notify.interval", 500000)
profile.set_preference("content.notify.ontimer", True)
profile.set_preference("content.switch.threshold", 250000)
profile.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
profile.set_preference("browser.startup.homepage", "about:blank")
profile.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
profile.set_preference("browser.pocket.enabled", False) # Duck pocket too!
profile.set_preference("loop.enabled", False)
profile.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
profile.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
profile.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
profile.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
profile.set_preference("browser.display.use_system_colors", True) # Use system colors.
profile.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
profile.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temprorary files.
profile.set_preference("browser.shell.checkDefaultBrowser", False)
profile.set_preference("browser.startup.homepage", "about:blank")
profile.set_preference("browser.startup.page", 0) # blank
profile.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
profile.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
profile.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.
profile.set_preference("browser.urlbar.showPopup", False) # Disable list of URLs when typing on URL bar.
profile.set_preference("browser.urlbar.showSearch", False) # Disable search bar.
profile.set_preference("extensions.checkCompatibility", False) # Addon update disabled
profile.set_preference("extensions.checkUpdateSecurity", False)
profile.set_preference("extensions.update.autoUpdateEnabled", False)
profile.set_preference("extensions.update.enabled", False)
profile.set_preference("general.startup.browser", False)
profile.set_preference("plugin.default_plugin_disabled", False)
profile.set_preference("permissions.default.image", 2) # Image load disabled again

profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

browser = webdriver.Firefox(firefox_profile=profile,
                           desired_capabilities=desired,
                            options=options)

def todays_message():
    messages_path = os.path.join(os.path.dirname(__file__), 'messages.txt')

    messages = []
    with open(messages_path, 'r') as f:
        raw_messages = f.read().split(sep='\n\n\n')
        for raw_message in raw_messages:
            messages.append({'date': pd.to_datetime(raw_message[:10]),
                             'message': raw_message[11:]})

    df = pd.DataFrame(messages)
    return df.loc[df['date'] == pd.to_datetime(date.today()), 'message'].iloc[0]


def send_message(recipient_number, message):
    log(f'{recipient_number}, starting browser.')
    browser.get('https://voice.google.com/u/0/messages')
    log(f'{recipient_number}, sleep 5')
    time.sleep(5)
    log(f'{recipient_number}, finding send new message')
    browser.find_element(By.XPATH, '//div[@gv-id="send-new-message"]').click()
    log(f'{recipient_number}, sleep 1')
    time.sleep(1)
    log(f'{recipient_number}, finding recipient picker input')
    elem = browser.find_element(By.XPATH, '//input[@gv-test-id="recipient-picker-input"]')
    log(f'{recipient_number}, sleep sending recipient')
    elem.send_keys(recipient_number)
    log(f'{recipient_number}, enter key')
    elem.send_keys(Keys.RETURN)
    log(f'{recipient_number}, finding textarea')
    elem = browser.find_element(By.TAG_NAME, 'textarea')
    log(f'{recipient_number}, entering message')
    elem.send_keys(message)
    log(f'{recipient_number}, enter key')
    elem.send_keys(Keys.RETURN)
    log(f'{recipient_number}, sleep 2')
    time.sleep(2)
    log(f'{recipient_number}, quiting')
    browser.quit()


    # try:
    #     elem = browser.find_element(By.XPATH, '//div[@class="gvBackdrop"]')
    #     elem.click()
    #     time.sleep(1)
    # except Exception as e:
    #     print('Backdrop Does not exist')

def get_recipients():
    recipients_path = os.path.join(os.path.dirname(__file__), 'recipients.csv')
    return pd.read_csv(recipients_path, header=None)

def send_daily_joy():
    today_message = todays_message()
    for index, recipient in get_recipients().iterrows():
        message = f"""Good morning, {recipient[1]}! Here's your Daily Joy:\n\n{today_message}"""
        send_message(recipient[0], message)

send_daily_joy()

browser.quit()


