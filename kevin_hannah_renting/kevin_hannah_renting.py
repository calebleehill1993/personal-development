from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import subprocess
import os
import pdfkit
import base64

housing_budget = 1400
morgage_payment = 740
morgage_rate = .04
starting_principle = 94000
annual_property_expenses = 1200
market_value_rent = 1800
total_years = 10

def calculate_benefit(months_kevin_renting, kevin_hannah_rent, end=False):
    monthly_rate = morgage_rate / 12
    kevin_hannah_monthly_savings = housing_budget - kevin_hannah_rent
    monthly_property_expenses = annual_property_expenses / 12
    mom_dad_income_monthly_with_kevin = kevin_hannah_rent - morgage_payment - monthly_property_expenses
    mom_dad_income_monthly_without_kevin = market_value_rent - morgage_payment - monthly_property_expenses

    # Columns: month, principle, i, payment, left_over_income, mom_dad_net, kevin_hannah_net, both net
    principle = np.zeros((120, 8))
    principle[0, 0] = 1
    principle[0, 1] = starting_principle
    principle[0, 2] = starting_principle * monthly_rate

    if principle[0, 0] <= months_kevin_renting:
        principle[0, 3] = mom_dad_income_monthly_with_kevin + morgage_payment
    else:
        principle[0, 3] = mom_dad_income_monthly_without_kevin + morgage_payment

    left_over = principle[0, 3] - principle[0, 1] - principle[0, 2]

    if left_over > 0:
        principle[0, 4] = left_over
    else:
        principle[0, 4] = 0

    principle[0, 5] = principle[0, 4] - principle[0, 1]

    principle[0, 6] = kevin_hannah_monthly_savings

    principle[0, 7] = principle[0, 5] + principle[0, 6]

    for i in range(1, total_years * 12):
        principle[i, 0] = i + 1

        if principle[i - 1, 4] > 0:
            principle[i, 1] = 0
        else:
            principle[i, 1] = principle[i - 1, 1] + principle[i - 1, 2] - principle[i - 1, 3]

        principle[i, 2] = principle[i, 1] * monthly_rate

        if principle[i, 0] <= months_kevin_renting:
            principle[i, 3] = mom_dad_income_monthly_with_kevin + morgage_payment
        else:
            principle[i, 3] = mom_dad_income_monthly_without_kevin + morgage_payment

        left_over = principle[i, 3] - principle[i, 1] - principle[i, 2]

        if left_over > 0:
            principle[i, 4] = principle[i - 1, 4] + left_over
        else:
            principle[i, 4] = 0

        principle[i, 5] = principle[i, 4] - principle[i, 1]

        if principle[i, 0] <= months_kevin_renting:
            principle[i, 6] = kevin_hannah_monthly_savings + principle[i - 1, 6]
        else:
            principle[i, 6] = principle[i - 1, 6]

        principle[i, 7] = principle[i, 5] + principle[i, 6]

    if end:
        kevin_hannah_total_savings = kevin_hannah_monthly_savings * months_kevin_renting

        return np.array([months_kevin_renting, principle[-1, 1], principle[-1, 4], principle[-1, 4] - principle[-1, 1] + starting_principle,
                         kevin_hannah_total_savings, principle[-1, 4] + kevin_hannah_total_savings + starting_principle - principle[-1, 1]])

    return principle

def currency_formatter(x):
    if x < 0:
        return "-${:,.2f}".format((np.abs(x)))
    else:
        return "${:,.2f}".format((x))

columns = ['Kevin/Hannah Housing Budget', 'Min Morgage Payment', 'Morgage Int. Rate', 'Starting Principle',
           'Annual Property Expenses', 'Market Value Rent']

parameters = pd.DataFrame([[housing_budget, morgage_payment, morgage_rate, starting_principle,
                           annual_property_expenses, market_value_rent]], columns=columns)

parameters[columns[0:2] + columns[3:]] = parameters[columns[0:2] + columns[3:]].applymap(currency_formatter)


data = np.zeros((10, 6))
data2 = np.zeros((10, 6))


for i in range(1, 11):
    data[i - 1] = calculate_benefit(i * 12, 1200, True)
    data2[i - 1] = calculate_benefit(i * 12, 840, True)

columns = ['Months with Kevin', 'Left on Morgage', 'Mom/Dad Saved', 'Mom/Dad Net Gain', 'Kevin Saved', 'All Net Gain']

data = pd.DataFrame(data, columns=columns)
data2 = pd.DataFrame(data2, columns=columns)

data['Months with Kevin'] = data['Months with Kevin'].astype(int)
data[columns[1:]] = data[columns[1:]].applymap(currency_formatter)

data2['Months with Kevin'] = data2['Months with Kevin'].astype(int)
data2[columns[1:]] = data2[columns[1:]].applymap(currency_formatter)

data.to_html('1200.html', index=False)
data2.to_html('840.html', index=False)

with open('kevin_hannah_renting.html', 'w') as w:
    w.write('<H1 class="table_title" style="font-size: 40; margin-bottom: 25px;">Kevin/Hannah Rent Scenarios</H1>\n')
    w.write('<H1 class="table_title">Parameters</H1>\n')
    w.write('<div style="margin-bottom: 40px">\n')
    w.write(parameters.to_html(index=False).replace('class="dataframe"', 'class="dataframe" style="margin-bottom: 5px"'))
    w.write('\n*Assuming all rent recieved during the 10 year period goes towards paying down the mortgage and then savings.</div>\n')
    with open('1200.html') as f:
        w.write('<H1 class="table_title">Results after 10 years with Kevin/Hannah Monthly Rent: $1200</H1>\n')
        w.write(f.read())
    with open('840.html') as f:
        w.write('<H1 class="table_title">Results after 10 years with Kevin/Hannah Monthly Rent: $840</H1>\n')
        w.write(f.read())

plt.rcParams["figure.figsize"] = (11, 8)

fig, ax = plt.subplots()

for j in range(5, 8):
    for i in range(12, 72, 12):
        data = calculate_benefit(i, 840)
        if j == 6:
            plt.plot(data[:, 0], data[:, j], linestyle='dotted',
                     label=f'\$840 for {i} months - {currency_formatter(data[119, j])}')
        else:
            plt.plot(data[:, 0], data[:, j] + starting_principle, linestyle='dotted',
                     label=f'\$840 for {i} months - {currency_formatter(data[119, j] + starting_principle)}')

    for i in range(60, 132, 12):
        data = calculate_benefit(i, 1200)
        if j == 6:
            plt.plot(data[:, 0], data[:, j],
                     label=f'\$1200 for {i} months - {currency_formatter(data[119, j])}')
        else:
            plt.plot(data[:, 0], data[:, j] + starting_principle,
                     label=f'\$1200 for {i} months - {currency_formatter(data[119, j] + starting_principle)}')


    if j == 5:
        fig.suptitle('Mom/Dad Net Savings', fontsize=24)
    if j == 6:
        fig.suptitle('Kevin/Hannah Net Savings', fontsize=24)
    if j == 7:
        fig.suptitle('All Net Savings', fontsize=24)
    plt.xlabel('Months in the Future')
    plt.ylabel('Savings')
    ticks = ax.get_yticks()
    ax.yaxis.set_major_locator(mticker.FixedLocator(ticks))
    new_labels = [currency_formatter(x) for x in ticks]
    ax.set_yticklabels(new_labels)
    plt.legend()
    plt.savefig(f'figure{j - 4}.png')
    plt.cla()

encoded1 = 'data:image/png;base64,' + base64.b64encode(open("figure1.png", "rb").read()).decode('utf-8')
encoded2 = 'data:image/png;base64,' + base64.b64encode(open("figure2.png", "rb").read()).decode('utf-8')
encoded3 = 'data:image/png;base64,' + base64.b64encode(open("figure3.png", "rb").read()).decode('utf-8')

with open('kevin_hannah_renting.html', 'a') as f:
    f.write(f'<img src="{encoded1}">')
    f.write(f'<img src="{encoded2}">')
    f.write(f'<img src="{encoded3}">')
    f.write('''<style>
    .dataframe {
        margin: auto;
        margin-bottom: 50;
    }
    
    td {
        text-align: right;
        padding: 3px
    }
    
    th {
        text-align: center;
        padding: 3px
    }
    
    .table_title {
        text-align: center;
        margin: auto;
    }
    
    img {
        max-width: 900;
        max-height: 600;
        text-align: center;
        margin: auto;
    }
    </style>''')

options = {
    'page-size': 'Letter',
    'margin-bottom': '10mm',
    'margin-left': '10mm',
    'margin-top': '10mm',
    'margin-right': '10mm'
}

pdfkit.from_url("kevin_hannah_renting.html", "kevin_hannah_renting.pdf", options=options)

# Remove files
os.remove('840.html')
os.remove('1200.html')
os.remove('figure1.png')
os.remove('figure2.png')
os.remove('figure3.png')

url = "kevin_hannah_renting.pdf"
# or a file on your computer
# url = "/Users/yourusername/Desktop/index.html
try: # should work on Windows
    os.startfile(url)
except AttributeError:
    try: # should work on MacOS and most linux versions
        subprocess.call(['open', url])
    except:
        print('Could not open URL')