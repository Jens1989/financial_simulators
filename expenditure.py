class NothundredpctError(Exception):
    pass

def testfn(value):

    if round(value,0) != 1:
        raise NothundredpctError("bla")


class Expenditure:
    
    def __init__(self, net_income):
        self.net_income = net_income # sum of the net salaries provided

    def fixed_expenditure(self, food=0, healthcare=0, mortgage=0, utilities=0, holidays=0, entertainment=0, restaurants=0, misc=0):
        self.food = food
        self.healthcare = healthcare
        self.mortgage = mortgage
        self.utilities = utilities
        self.holidays = holidays
        self.entertainment = entertainment 
        self.restaurants = restaurants
        self.misc = misc

    def percentual_expenditure(self, food_pct=0, healthcare_pct=0, mortgage_pct=0, utilities_pct=0, holidays_pct=0, entertainment_pct=0, restaurants_pct=0, misc_pct=0, savings_pct=0):
        
        try:
            testfn(sum((food_pct, healthcare_pct, mortgage_pct, holidays_pct, entertainment_pct, restaurants_pct, entertainment_pct, misc_pct, savings_pct)))
        except NothundredpctError as e:
            print(f"the total doesn't add up to 100%, it's currently {sum((food_pct, healthcare_pct, mortgage_pct, holidays_pct, entertainment_pct, restaurants_pct, entertainment_pct, misc_pct, savings_pct))}00%")
        self.food_pct = food_pct
        self.healthcare_pct = healthcare_pct
        self.mortgage_pct = mortgage_pct
        self.utilities_pct = utilities_pct
        self.holidays_pct = holidays_pct
        self.entertainment_pct = entertainment_pct
        self.restaurants_pct = restaurants_pct
        self.misc_pct = misc_pct
        self.savings_pct = savings_pct

        self.food = self.net_income * food_pct
        self.healthcare = self.net_income * healthcare_pct
        self.mortgage = self.net_income * mortgage_pct
        self.utilities = self.net_income * utilities_pct
        self.holidays = self.net_income * holidays_pct
        self.entertainment = self.net_income * entertainment_pct
        self.restaurants = self.net_income * restaurants_pct
        self.misc = self.net_income * misc_pct
        self.savings = self.net_income * savings_pct

if __name__ == "__main__":
    test = Expenditure(6200)
    test.percentual_expenditure(food_pct=0.2, healthcare_pct= 0.01, mortgage_pct=0.3, utilities_pct=0.05, holidays_pct=0.05, entertainment_pct=0.05, restaurants_pct=0.05, misc_pct=0.09, savings_pct=0.2)
    print(test.mortgage)

