from tabulate import tabulate

class Salary:
    def __init__(self, salary, tax_credits):
        self.gross_salary = salary 
        self.pretax_salary = salary
        self.prsi = self._apply_prsi(self.gross_salary)
        self.usc = self._apply_usc(self.gross_salary)
        self.tax_credits = tax_credits
        self.post_tax_amount = 0

    def add_post_tax_amount(self, amount):
        self.post_tax_amount = amount # for example life insurance

    def monthly_net_salary(self, annual_pension_contribution_pct):

        self._pension_contribution(annual_pension_contribution_pct)
        self._apply_tax_bands(self.pretax_salary)

        annual_net_salary = self.pretax_salary - self.prsi - self.usc - self.paye + self.tax_credits - self.post_tax_amount
        monthly_net_salary = annual_net_salary / 12

        return monthly_net_salary

    def show_salary_breakedown(self, net_salary):
        table = [['Description', 'Amount'], ['gross salary', self.gross_salary/12], ['pretax salary', self.pretax_salary/12], ['prsi', self.prsi/12], ['usc', self.usc/12], ['post tax adjustment', self.post_tax_amount/12], ['net salary', net_salary]]
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))  

    def _pension_contribution(self, annual_pension_contribution_pct):
        self.pretax_salary = self.gross_salary * (1-annual_pension_contribution_pct)
        self.annual_pension_contribution = self.gross_salary * annual_pension_contribution_pct 

    def _apply_prsi(self, gross_salary):
        '''https://www.citizensinformation.ie/en/social-welfare/irish-social-welfare-system/social-insurance-prsi/paying-social-insurance/#:~:text=You%20work%20out%20how%20much,at%204%25%20of%20your%20earnings.'''
        prsi =  gross_salary *.04 
        return prsi 

    def _apply_usc(self, gross_salary):
        '''https://www.revenue.ie/en/jobs-and-pensions/usc/standard-rates-thresholds.aspx
        '''
        usc = 0 
        balance = gross_salary
        if balance > 70044: # above 70044 taxed at 8%
            usc += (balance - 70044) * .08
            balance = 70044
        if balance > 22920: # next 47124 taxed at 4.5%
            usc += (balance - 22920) * 0.045
            balance = 22920
        if balance > 12012: # next 10908 taxed at 2%
            usc += (balance - 10908) * 0.02
            balance = 12012
        if balance <= 12012: # last 12012 taxed at 0.5%
            usc += balance * 0.005
            balance = 0 
        
        return usc

    def _apply_tax_bands(self, applicable_salary):
        if applicable_salary > 49000:
            paye = 49000 * 0.2 + (applicable_salary - 49000) * 0.4 # first 49k @ 20% and everything above @ 40%
        self.paye = paye


if __name__ == "__main__":
    test = Salary(70000, 6032)
    test.add_post_tax_amount(159.54*12) # health insurance
    print(test.monthly_net_salary(.05))
    test.show_salary_breakedown(test.monthly_net_salary(.05))
