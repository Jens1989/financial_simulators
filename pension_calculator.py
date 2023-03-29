import streamlit as st

st.set_page_config(layout="wide")

st.title('Pension Calculator')

left_column, right_column = st.columns(2)

with left_column:
    starting_capital = st.number_input("Starting Capital: ", key = int)
    salary = st.number_input("Starting Salary : ", 0,100000 ) 

with right_column:

    bonus_pct = st.number_input("Bonus %: ", 0, 100 ) / 100 
    annual_salary_increase = st.number_input("Salary Increase %: ", 0, 100 ) / 100 
    annual_return = st.number_input("Annual Return %: ", 0, 100 ) / 100 

years = 30
inflation = 0.02
management_fee = 0.0075

capital_series = [starting_capital]

for i in range(years-1):

    salary = salary * (1+annual_salary_increase)

    contribution = 0

    if salary < 113000:
        contribution = salary*.2 + salary * .1  
    else:
        contribution = 113000*.2 + salary *.1
    
    contribution += round(salary * bonus_pct,0)
    
    growth = round(capital_series[-1] * (1+annual_return-management_fee),0)

    capital_series.append(contribution + growth)

st.write(f'The amount at retirement = {int(capital_series[-1]):,} ' )

st.line_chart(capital_series)
