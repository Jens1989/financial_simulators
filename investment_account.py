import matplotlib.pyplot as plt


class InvestmentAccount:
    def __init__(self, balance, annual_return, management_fee_pct):
        self.balance = balance
        self.monthly_return = annual_return/12
        self.management_fee_pct = management_fee_pct # annual brokerage fee

    def calculate_returns(self):
        return self.balance * (1 + self.monthly_return)

class PensionInvestmentAccount:
    def __init__(self, balance, monthly_contribution, bonus_contribution, annual_return, management_fee_pct):
        self.balance = balance
        self.monthly_contribution = monthly_contribution
        self.bonus_contribution = bonus_contribution
        self.monthly_return = annual_return/12
        self.management_fee_pct = management_fee_pct # annual brokerage fee

    def update_balance(self, end_of_year: bool): # end of year is used to apply the annual management fee and bonus

        self._calculate_returns()
        self._add_contribution()

        if end_of_year:
            self._add_bonus_contribution()
            self._deduct_management_fee()

    def _calculate_returns(self):
        self.balance = self.balance * (1 + self.monthly_return)

    def _add_contribution(self):
        self.balance = self.balance + self.monthly_contribution

    def _add_bonus_contribution(self):
        self.balance = self.balance + self.bonus_contribution

    def _deduct_management_fee(self):
        self.balance = self.balance * (1-self.management_fee_pct)


if __name__ == "__main__":
    test = PensionInvestmentAccount(70000, 800, 15000, 0.05, 0.0075)

    l = [test.balance] 

    for i in range(1,120+1):
        if i % 12 == 0: # end of year
            test.update_balance(True)
 
            print(int(test.balance))
        else:
            test.update_balance(False)

        l.append(test.balance)
    
    plt.plot(l)
    plt.show()