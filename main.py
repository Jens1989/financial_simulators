import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from investment_account import PensionInvestmentAccount
from salary import Salary
from mortgage_calculator import mortgage_calculator

class Simulation:
    def __init__(self, net_worth):
        self.investment_accounts = []
        self.properties = []
        self.salaries = []
        self.net_worth = net_worth

    def add_investment_account(self, account):
        self.investment_accounts.append(account)

    def add_property(self, prop):
        self.properties.append(prop)

    def add_salary(self, salary):
        self.salaries.append(salary)

    def run_simulation(self, years):
        num_months = years * 12
        net_worth_over_time = []
        property = self.properties[0]
        sal = self.salaries[0]
        sal.add_post_tax_amount(159.54*12)
        net_salary = sal.monthly_net_salary(.05)

        principal = property.principal

        total_net_worth = sum(account.balance for account in self.investment_accounts) + property.principal

        for month in range(1, num_months+1):
            if month % 12 == 0: # end of year
                self.investment_accounts[0].update_balance(True)
                investment_balance = sum(account.balance for account in self.investment_accounts) 
            else:
                self.investment_accounts[0].update_balance(False)

                investment_balance = sum(account.balance for account in self.investment_accounts) 

            property.amortization_schedule()
            principal += property.principal
            net_salary += sal.monthly_net_salary(.05)
            total_net_worth = net_salary + principal + investment_balance
            net_worth_over_time.append(total_net_worth)

        return net_worth_over_time

def plot_graph(x_values, y_values, title, xlabel, ylabel):
    plt.figure()
    plt.plot(x_values, y_values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def on_run_simulation_button():
    # Fetch user inputs and create objects
    # ...

    overpayment_amount = int(overpayment_amount_entry.get())

    simulation = Simulation(0)
    simulation.add_investment_account(PensionInvestmentAccount(67000, 875, 15000, 0.05, 0.0075))
    simulation.add_property(mortgage_calculator(375000, 30, 0.0405, overpayment_amount = overpayment_amount, overpayment_years = 10))
    simulation.add_salary(Salary(70000,6000))
    # Add investment accounts, properties, and salaries to the simulation
    # ...

    years = int(years_entry.get())  # Get simulation duration from GUI input
    net_worth_over_time = simulation.run_simulation(years)
    x_values = np.arange(1, years * 12 + 1)
    
    plot_graph(x_values, net_worth_over_time, "Net Worth Over Time", "Months", "Net Worth")

# Create GUI
root = tk.Tk()
root.title("Financial Simulator")

# Create and place GUI elements
years_label = ttk.Label(root, text="Simulation Duration (Years)")
years_label.grid(row=0, column=0)
years_entry = ttk.Entry(root)
years_entry.grid(row=0, column=1)

overpayment_amount_label = ttk.Label(root, text="Overpayment Amount (Monthly)")
overpayment_amount_label.grid(row=1, column=0)
overpayment_amount_entry = ttk.Entry(root)
overpayment_amount_entry.grid(row=1, column=1)

run_button = ttk.Button(root, text="Run Simulation", command=on_run_simulation_button)
run_button.grid(row=2, columnspan=2)

# Start the GUI event loop
root.mainloop()
