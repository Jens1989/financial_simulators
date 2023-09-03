import pandas as pd

# st.set_page_config(layout="wide")

# st.title('Mortgage Calculator')

# left_column, right_column = st.columns(2)

# with left_column:
#     mortgage_amount = int(st.number_input("Mortgage Amount: ", value= 300000))
#     mortgage_term = int(st.number_input("Mortgage Term : ", value = 20))
#     overpay_years = int(st.number_input("Overpaying principal term : ", value = 0))
#     overpay_amount = int(st.number_input("Overpayment Amount : ", value = 0))

# with right_column:

#     interest_rate = st.number_input("Interest Rate %: ", 0.0, 100.0, value = 2.9) / 100 

class mortgage_calculator:

    def __init__(self, balance, mortgage_term, interest_pct, overpayment_amount = 0, overpayment_years = 0):
        self.balance = balance
        self.mortgage_term = mortgage_term
        self.interest_pct = interest_pct
        self.overpayment_amount = overpayment_amount
        self.overpayment_years = overpayment_years
        self.monthly_payment = self._monthly_payment(self.interest_pct, self.mortgage_term, self.balance)
        self.interest_amt = self._interest_amount_calc(self.balance, self.interest_pct)
        self.principal = self._principal(self.monthly_payment, self.interest_amt)
        self.end_balance = self._end_balance(self.balance, self.principal)

# balance = [mortgage_amount]
# interest = [interest_amount_calc(mortgage_amount, interest_rate)]
# monthly_payment = pmt(interest_rate/12,12*mortgage_term,-mortgage_amount)
# principal = [monthly_payment-interest[-1]]
# ending_balance = [mortgage_amount-principal[-1]]

# overpayment_payment_series = [overpay_amount]

    def calculate(self):

        balance_series = [self.balance]
        interest_series = [self.interest_amt]
        monthly_payment_series = [self.monthly_payment]
        principal_series = [self.principal]
        end_balance_series = [self.end_balance]
        overpayment_series = [self.overpayment_amount]

        for i in range(self.mortgage_term*12-1): # loop over every month

            if i%12 == 0:
                if self.overpayment_amount*12 <= self.end_balance * .1: # can maximum overpay 10% of the outstanding balance
                    pass
                else:
                    self.overpayment_amount = round(self.end_balance*.1/12,0) 
            else:
                pass

            if self.end_balance > 0:
                self.principal = self._principal(self.monthly_payment, self.interest_pct, self.overpayment_amount)
                self.end_balance = self._end_balance(self.balance, self.principal)
                balance_series.append(self.end_balance)
            else:
                balance_series.append(0)

            self._interest_amount_calc(self.balance, self.interest_pct)
            interest_series.append(self.interest_amt)

            if i < self.overpayment_years * 12:
                self._principal(self.monthly_payment, self.interest_amt, self.overpayment_amount)
                principal_series.append(self.principal)
                end_balance_series.append(self.balance-self.principal-self.overpayment_amount)
                overpayment_series.append(round(self.overpayment_amount,0))
            else:
                self._principal(self.monthly_payment, self.interest_amt)
                principal_series.append(self.principal)
                self._end_balance(self.balance, self.principal)
                end_balance_series.append(self.end_balance)
                overpayment_series.append(0)
            

        interest = [round(x) for x in interest_series]
        principal = [round(x) for x in principal_series]
        ending_balance = [round(x) for x in end_balance_series]
        balance = [round(x) for x in balance_series]

        df = pd.DataFrame({'Starting Balance': balance,
                    'Interest': interest,
                    'Principal': principal,
                    'Ending Balance': ending_balance,
                    'Overpayment Amount': overpayment_series})

        return df

    def _pmt(self, rate, nper, pv, fv=0, type=0):
        """
        Calculates the payment for a loan based on constant payments and a constant interest rate.

        Parameters
        ----------
        rate : float
            Interest rate for each period.
        nper : int
            Total number of payment periods.
        pv : float
            Present value, or the amount of the loan.
        fv : float, optional
            Future value, or the cash balance you want after the last payment is made. Default is 0.
        type : {0, 1}, optional
            When payments are due. 0 for end of period (default), 1 for beginning of period.

        Returns
        -------
        pmt : float
            Payment for each period.
        """

        if rate == 0:
            return -(fv + pv) / nper

        if type not in (0, 1):
            raise ValueError("Type must be 0 or 1.")

        pmt = -rate * (fv + pv * (1 + rate) ** nper) / ((1 + rate * type) * ((1 + rate) ** nper - 1))

        return pmt

    def _interest_amount_calc(self, starting_balance, rate):
        return starting_balance*rate/12

    def _monthly_payment(self, interest_rate, mortgage_term, balance):
        return self._pmt(interest_rate/12, 12*mortgage_term,-balance)

    def _principal(self, monthly_payment, interest, overpayment_amount = 0):
        return monthly_payment - interest - overpayment_amount

    def _end_balance(self, balance, principal):
        return balance - principal



# st.write(df)

# st.write(f'total interest paid: {sum(interest)}')
# st.write(f'Monthly Payment : {int(monthly_payment)}')

if __name__ == '__main__':
    test = mortgage_calculator(375000, 30, 4.05)
    print(test.calculate())