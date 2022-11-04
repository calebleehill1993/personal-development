
# Used for requesting URLs with HTTP protocol
import requests

# Used for scrapping websites from HTML
from bs4 import BeautifulSoup

# Pandas is used to store and manipulate data
import pandas as pd

def get_state_populations():
    url = 'https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_population'
    response = requests.get(url=url)

    # The content of the request is simply the html file's text as a string
    response.content

    # The name soup is more historical than having any real meaning. It basically just refers to
    # the potential soupy mess that can be called HTML

    # The BeautifulSoup object is just a nested data structure with various methods that are useful
    # for scraping and parsing HTML documents among other things.
    soup = BeautifulSoup(response.content, 'html.parser')

    # We can view our soup made pretty!
    print(soup.prettify())

    # We can use the find_all method to return a list of all of a specified tag
    # 'a' is the tag used for links
    soup.find_all('a')

    # It's usually helpful to know exactly what you are looking for so I usually use
    # the dev tools of Google Chrome or another browser to search the HTML quickly to find
    # what I'm looking for.

    # In this case, I want the first table on the page
    table = soup.find('table')

    print(table.prettify())

    (type(table), len(table))

    # Then I want the table body
    tbody = table.find('tbody')

    (type(tbody), len(tbody))

    data = []
    columns = ['Rank 2021', 'Rank 2010', 'State or Territory', '2021 Population', '2010 Population',
               '% Change', 'Abs. Change', 'House of Reps', 'House %', 'Pop per Electoral Vote 2020',
               'Pop per seat 2020', 'Pop per seat 2010', '% of total US pop 2020', '% of total US pop 2021',
               'Change in % total', '% of electoral college']

    # Then I want to go through each row in the table
    for row in tbody.find_all('tr'):
        # We put the cell values in a list
        row_data = []

        # We want to skip the table head and just get the data
        if row.contents[1].name == 'th':
            continue

        # We go through each cell in each row
        for cell in row:
            # Some cells have nested HTML that we want to strip for just the text value of the cell
            if cell.name == 'th':
                row_data.append(cell.find('a').text.strip())
            else:
                if len(cell.text.strip()) > 0:
                    row_data.append(cell.text.strip().replace(',', ''))

        print(row_data, len(row_data))
        data.append(row_data)

    df = pd.DataFrame(data=data, columns=columns)
    df

    df.to_csv('population_data.csv', index=False)
    df.to_json('population_data.json')

if __name__ == '__main__':
    get_state_populations()

