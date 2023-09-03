import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from investment_account import PensionInvestmentAccount

class Property:
    def __init__(self, value, mortgage_amount, interest_rate, overpayment_option):
        self.value = value
        self.mortgage_amount = mortgage_amount
        self.interest_rate = interest_rate
        self.overpayment_option = overpayment_option

    def calculate_monthly_payment(self):
        monthly_rate = self.interest_rate / 12 / 100
        num_payments = 12 * 30  # 30-year mortgage
        monthly_payment = self.mortgage_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        return monthly_payment

class Salary:
    def __init__(self, net_salary, annual_increase, bonus_percentage):
        self.net_salary = net_salary
        self.annual_increase = annual_increase
        self.bonus_percentage = bonus_percentage

    def calculate_monthly_cash_flow(self):
        return self.net_salary / 12

class Simulation:
    def __init__(self):
        self.investment_accounts = []
        self.properties = []
        self.salaries = []

    def add_investment_account(self, account):
        self.investment_accounts.append(account)

    def add_property(self, prop):
        self.properties.append(prop)

    def add_salary(self, salary):
        self.salaries.append(salary)

    def run_simulation(self, years):
        num_months = years * 12
        net_worth_over_time = []

        for month in range(num_months):
            total_net_worth = sum(account.balance for account in self.investment_accounts)
            total_net_worth += sum(prop.value for prop in self.properties)
            total_net_worth += sum(salary.net_salary for salary in self.salaries)

            net_worth_over_time.append(total_net_worth)

            for account in self.investment_accounts:
                account.deduct_fees()
                account.balance = account.calculate_returns()

            for prop in self.properties:
                monthly_payment = prop.calculate_monthly_payment()
                prop.mortgage_amount -= monthly_payment

            for salary in self.salaries:
                salary.net_salary *= 1 + salary.annual_increase / 100

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

    simulation = Simulation()
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

run_button = ttk.Button(root, text="Run Simulation", command=on_run_simulation_button)
run_button.grid(row=1, columnspan=2)

# Start the GUI event loop
root.mainloop()
