import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title('Mortgage Calculator')

left_column, right_column = st.columns(2)

with left_column:
    mortgage_amount = int(st.number_input("Mortgage Amount: ", value= 300000))
    mortgage_term = int(st.number_input("Mortgage Term : ", value = 20))
    overpay_years = int(st.number_input("Overpaying principal term : ", value = 0))
    overpay_amount = int(st.number_input("Overpayment Amount : ", value = 0))

with right_column:

    interest_rate = st.number_input("Interest Rate %: ", 0.0, 100.0, value = 2.9) / 100 

def pmt(rate, nper, pv, fv=0, type=0):
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

def interest_amount_calc(starting_balance, rate):
    return starting_balance*rate/12

balance = [mortgage_amount]
interest = [interest_amount_calc(mortgage_amount, interest_rate)]
monthly_payment = pmt(interest_rate/12,12*mortgage_term,-mortgage_amount)
principal = [monthly_payment-interest[-1]]
ending_balance = [mortgage_amount-principal[-1]]

overpayment_payment_series = [overpay_amount]


for i in range(mortgage_term*12-1):

    if i%12 == 0:
        if overpay_amount*12 <= ending_balance[-1] * .1: # can maximum overpay 10% of the outstanding balance
            pass
        else:
            overpay_amount = round(ending_balance[-1]*.1/12,0)
    else:
        pass

    if ending_balance[-1] > 0:
        balance.append(ending_balance[-1])
    else:
        balance.append(0)

    interest.append(interest_amount_calc(balance[-1], interest_rate ))

    if i < overpay_years * 12:
        principal.append(monthly_payment-interest[-1] + overpay_amount)
        ending_balance.append(balance[-1]-principal[-1] - overpay_amount)
        overpayment_payment_series.append(round(overpay_amount,0))
    else:
        principal.append(monthly_payment-interest[-1])
        ending_balance.append(balance[-1]-principal[-1])
        overpayment_payment_series.append(0)
    

    interest = [round(x) for x in interest]
    principal = [round(x) for x in principal]
    ending_balance = [round(x) for x in ending_balance]
    balance = [round(x) for x in balance]

df = pd.DataFrame({'Starting Balance': balance,
             'Interest': interest,
             'Principal': principal,
             'Ending Balance': ending_balance,
             'Overpayment Amount': overpayment_payment_series})

st.write(df)

st.write(f'total interest paid: {sum(interest)}')
st.write(f'Monthly Payment : {int(monthly_payment)}')