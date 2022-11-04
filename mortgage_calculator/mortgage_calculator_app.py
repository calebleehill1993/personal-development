# used pyinstaller to create an executable file
# https://datatofish.com/executable-pyinstaller/
# pyinstaller --onefile mortgage_calculator_app.py
# This did not work on MacOS very well

import numpy as np
from tkinter import *

def currency_formatter(x):
    if x < 0:
        return "-${:,.2f}".format((np.abs(x)))
    else:
        return "${:,.2f}".format((x))

class MyWindow:
    def __init__(self, win):
        # The Parameters
        self.home_price = 400000
        self.down_payment = 20000
        self.loan_amount = 380000
        self.percent_down = .05
        self.annual_interest_rate = .06
        self.loan_years = 30
        self.property_tax_rate = .0056
        self.annual_pmi_rate = .01
        # Just taking a high Idaho Estimate (About the National Average)
        self.annual_homeowner_insurance = 1200
        self.square_feet = 2000

        self.lbl_home_price = Label(win, text='Home Price')
        self.lbl_home_price.place(x=100, y=50)
        self.t_home_price = Entry()
        self.t_home_price.place(x=300, y=50)
        self.t_home_price.insert(0, str(self.home_price))
        
        self.lbl_loan_amount = Label(win, text='Loan Amount')
        self.lbl_loan_amount.place(x=500, y=50)
        self.t_loan_amount = Entry()
        self.t_loan_amount.place(x=700, y=50)
        self.t_loan_amount.insert(0, currency_formatter(self.loan_amount))
        self.t_loan_amount.bind("<Key>", lambda e: "break")
        
        self.lbl_down_payment = Label(win, text='Down Payment')
        self.lbl_down_payment.place(x=100, y=100)
        self.t_down_payment = Entry()
        self.t_down_payment.place(x=300, y=100)
        self.t_down_payment.insert(0, str(self.down_payment))
        
        self.lbl_percent_down = Label(win, text='Percent Down')
        self.lbl_percent_down.place(x=500, y=100)
        self.t_percent_down = Entry()
        self.t_percent_down.place(x=700, y=100)
        self.t_percent_down.insert(0, str(self.percent_down))

        self.lbl_annual_interest_rate = Label(win, text='Annual Interest Rate')
        self.lbl_annual_interest_rate.place(x=100, y=150)
        self.t_annual_interest_rate = Entry()
        self.t_annual_interest_rate.place(x=300, y=150)
        self.t_annual_interest_rate.insert(0, str(self.annual_interest_rate))

        self.lbl_loan_years = Label(win, text='Years of Loan')
        self.lbl_loan_years.place(x=100, y=200)
        self.t_loan_years = Entry()
        self.t_loan_years.place(x=300, y=200)
        self.t_loan_years.insert(0, str(self.loan_years))
        
        self.lbl_property_tax_rate = Label(win, text='Property Tax Rate')
        self.lbl_property_tax_rate.place(x=100, y=250)
        self.t_property_tax_rate = Entry()
        self.t_property_tax_rate.place(x=300, y=250)
        self.t_property_tax_rate.insert(0, str(self.property_tax_rate))
        
        self.lbl_monthly_property_tax = Label(win, text='Monthly Property Tax')
        self.lbl_monthly_property_tax.place(x=500, y=250)
        self.t_monthly_property_tax = Entry()
        self.t_monthly_property_tax.place(x=700, y=250)
        self.t_monthly_property_tax.insert(0, currency_formatter(self.monthly_property_tax(self.home_price)))
        self.t_monthly_property_tax.bind("<Key>", lambda e: "break")

        self.lbl_annual_pmi_rate = Label(win, text='Annual PMI Rate')
        self.lbl_annual_pmi_rate.place(x=100, y=300)
        self.t_annual_pmi_rate = Entry()
        self.t_annual_pmi_rate.place(x=300, y=300)
        self.t_annual_pmi_rate.insert(0, str(self.annual_pmi_rate))
        
        self.lbl_monthly_pmi = Label(win, text='Monthly PMI')
        self.lbl_monthly_pmi.place(x=500, y=300)
        self.t_monthly_pmi = Entry()
        self.t_monthly_pmi.place(x=700, y=300)
        self.t_monthly_pmi.insert(0, currency_formatter(self.monthly_pmi()))
        self.t_monthly_pmi.bind("<Key>", lambda e: "break")

        self.lbl_annual_homeowner_insurance = Label(win, text='Annual Homeowner Insurance')
        self.lbl_annual_homeowner_insurance.place(x=100, y=350)
        self.t_annual_homeowner_insurance = Entry()
        self.t_annual_homeowner_insurance.place(x=300, y=350)
        self.t_annual_homeowner_insurance.insert(0, str(self.annual_homeowner_insurance))
        
        self.lbl_monthly_homeowner_insurance = Label(win, text='Monthly Homeowner Insurance')
        self.lbl_monthly_homeowner_insurance.place(x=500, y=350)
        self.t_monthly_homeowner_insurance = Entry()
        self.t_monthly_homeowner_insurance.place(x=700, y=350)
        self.t_monthly_homeowner_insurance.insert(0, currency_formatter(self.monthly_homeowner_insurance()))
        self.t_monthly_homeowner_insurance.bind("<Key>", lambda e: "break")
        
        self.lbl_square_feet = Label(win, text='Home Square Footage')
        self.lbl_square_feet.place(x=100, y=400)
        self.t_square_feet = Entry()
        self.t_square_feet.place(x=300, y=400)
        self.t_square_feet.insert(0, str(self.square_feet))

        self.lbl_monthly_maintenance = Label(win, text='Monthly Maintenance')
        self.lbl_monthly_maintenance.place(x=500, y=400)
        self.t_monthly_maintenance = Entry()
        self.t_monthly_maintenance.place(x=700, y=400)
        self.t_monthly_maintenance.insert(0, currency_formatter(self.monthly_property_maintenance()))
        self.t_monthly_maintenance.bind("<Key>", lambda e: "break")

        self.b_calculate_mortgage = Button(win, text='Calculate Mortgage', command=self.show_mortgage)
        self.b_calculate_mortgage.place(x=100, y=450)

        self.lbl_base_mortgage_payment = Label(win, text='Base Mortgage Payment')
        self.lbl_base_mortgage_payment.place(x=100, y=500)
        self.t_base_mortgage_payment = Entry()
        self.t_base_mortgage_payment.place(x=300, y=500)
        self.t_base_mortgage_payment.bind("<Key>", lambda e: "break")
        
        self.lbl_extra_fees = Label(win, text='Extra Fees')
        self.lbl_extra_fees.place(x=500, y=500)
        self.t_extra_fees = Entry()
        self.t_extra_fees.place(x=700, y=500)
        self.t_extra_fees.bind("<Key>", lambda e: "break")
        
        self.lbl_total_mortgage_payment = Label(win, text='Total Mortgage Payment')
        self.lbl_total_mortgage_payment.place(x=100, y=550)
        self.t_total_mortgage_payment = Entry()
        self.t_total_mortgage_payment.place(x=300, y=550)
        self.t_total_mortgage_payment.bind("<Key>", lambda e: "break")
        
        self.lbl_total_mortgage_payment_no_pmi = Label(win, text='Total Mortgage Payment No PMI')
        self.lbl_total_mortgage_payment_no_pmi.place(x=100, y=600)
        self.t_total_mortgage_payment_no_pmi = Entry()
        self.t_total_mortgage_payment_no_pmi.place(x=300, y=600)
        self.t_total_mortgage_payment_no_pmi.bind("<Key>", lambda e: "break")

    def set_parameters(self):
        self.home_price = float(self.t_home_price.get())
        self.down_payment = float(self.t_down_payment.get())
        self.loan_amount = self.home_price - self.down_payment
        self.annual_interest_rate = float(self.t_annual_interest_rate.get())
        self.loan_years = float(self.t_loan_years.get())
        self.property_tax_rate = float(self.t_property_tax_rate.get())
        self.annual_pmi_rate = float(self.t_annual_pmi_rate.get())
        self.annual_homeowner_insurance = float(self.t_annual_homeowner_insurance.get())
        self.square_feet = float(self.t_square_feet.get())

    def show_mortgage(self):
        self.set_parameters()
        self.t_base_mortgage_payment.delete(0, END)
        self.t_base_mortgage_payment.insert(END, currency_formatter(self.mortgage()))
        self.t_extra_fees.delete(0, END)
        self.t_extra_fees.insert(END, currency_formatter(self.mortgage(base=False, tax=True, maintenance=True,
                                                                                   pmi=True, homeowner_insurance=True)))
        self.t_total_mortgage_payment.delete(0, END)
        self.t_total_mortgage_payment.insert(END, currency_formatter(self.mortgage(tax=True, maintenance=True,
                                                                                   pmi=True, homeowner_insurance=True)))
        self.t_total_mortgage_payment_no_pmi.delete(0, END)
        self.t_total_mortgage_payment_no_pmi.insert(END, currency_formatter(self.mortgage(tax=True, maintenance=True,
                                                                                   pmi=False, homeowner_insurance=True)))

    
    def monthly_homeowner_insurance(self):
        return self.annual_homeowner_insurance / 12

    def annual_pmi(self):
        return self.loan_amount * self.annual_pmi_rate
    
    def monthly_pmi(self):
        return self.annual_pmi() / 12

    def annual_property_tax(self, market_value):
        return market_value * self.property_tax_rate
    
    def monthly_property_tax(self, market_value):
        return self.annual_property_tax(market_value) / 12

    def annual_property_maintenance(self):
        return self.square_feet
    
    def monthly_property_maintenance(self):
        return self.annual_property_maintenance() / 12

    def mortgage(self, base=True, tax=False, maintenance=False, pmi=False, homeowner_insurance=False):
        monthly_i = self.annual_interest_rate / 12
        months = self.loan_years * 12

        mortgage = 0

        if base:
            mortgage += (self.loan_amount * monthly_i * (1 + monthly_i) ** months) / ((1 + monthly_i) ** months - 1)

        if tax:
            mortgage += self.monthly_property_tax(self.home_price)

        if maintenance:
            mortgage += self.monthly_property_maintenance()

        if pmi:
            mortgage += self.monthly_pmi()

        if homeowner_insurance:
            mortgage += self.monthly_homeowner_insurance()

        return mortgage

    def total_interest_paid(self, principle, i, payment):
        monthly_i = i / 12
        total_interest_paid = 0
        months = 0

        if principle * monthly_i >= payment:
            return 99999999999999999

        current_principle = principle
        while current_principle > 0:
            current_interest = current_principle * monthly_i
            paid_on_principle = payment - current_interest
            total_interest_paid += current_interest
            current_principle -= paid_on_principle
            months += 1

        return {'total_interest': total_interest_paid, 'months': months}


window=Tk()
mywin=MyWindow(window)
window.title('Mortgage Calculator')
window.geometry("1000x700+10+10")
window.mainloop()