import pandas as pd
import requests
from sklearn.svm import SVR

from datetime import datetime
from datetime import timedelta

def history(ndays):
    """gets and displays historical data

    Arguments:
        ndays {int} -- number of days
    """    
    today = datetime.today().date() - timedelta(days=int(ndays))
    today = today.strftime("%m-%d-%Y")
    covid_data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+today+".csv")
    covid_data = covid_data[['Province_State', 'Country_Region', 'Confirmed', 'Deaths', 'Recovered', 'Active']]
    print("Data from ", today)
    print(covid_data.sort_values(by='Country_Region', ascending=True))

def prediction(country):
    """predicts tommorows covid19 active casses for specific cuntry using machine learing linear regression model

    Arguments:
        country {strng} -- specific country
    """    
    user = input("\nWould you like to see tommorow active casses prediction for this country? (y/n):\n").upper()
    if user == "Y":
        data_set = []
        print("Calculating...")
        for n in range(1,51):
            today = datetime.today().date() - timedelta(days=n)
            today = today.strftime("%m-%d-%Y")
            covid_data= pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+today+".csv")
            covid_data = covid_data.loc[covid_data['Country_Region'] == country]
            data_set.append(covid_data['Active'].item())

        df = pd.DataFrame(data_set, columns=['Active'])
        df = df.iloc[::-1]
        df['Pred'] = df['Active'].shift(-1)
        pred = []
        active = []
        df = df.head(len(df)-1)
        df_active = df.loc[:, 'Active']
        df_pred = df.loc[:, 'Pred']
        for x in df_active:
            active.append([int(x)])
        for y in df_pred:
            pred.append(int(y))

        svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
        #Train the SVR models 
        svr_rbf.fit(active,pred)
        p = svr_rbf.predict([[int(df['Pred'].tail(1))]])[0]
        print("Predicted active casses in %s for tommorow is %d" % (country,p))
    else:
        menu()


def get_data(country):
    """gets data from api

    Returns:
        json as string -- converts json to string
    """
    data = pd.read_json(requests.get("https://coronavirus-19-api.herokuapp.com/countries/").text)
    if country =="top10":
        print(data.sort_values(by='cases', ascending=False)[1:11])
    elif country !="":
        if data.loc[data['country'] == country].empty == False:
            print(data.loc[data['country'] == country])
            prediction(country)
        else:
            print("\nNo such country\n")
            menu()
    else:
        print(data.sort_values(by='country', ascending=True)) 

def menu(): 
    """Display initial menu to user"""

    menuChoice = ""
    menuChoice = input('1.Poland live statistics\n2.World wide statiscics\n3.Country wide statiscics\n4.Choose country\n5.Top 10 cuntries data\n6.Historical data\n7.Quit\n\n')

    if menuChoice == "1" :
        get_data("Poland")
    elif menuChoice == "2" :
        get_data("World")
    elif menuChoice == "3" :
        get_data("")
    elif menuChoice == "4" :
        country = input("\nType in name of the country that you wish to see statistics for:\n").capitalize()
        get_data(country)
    elif menuChoice == "5" :
        get_data("top10")
    elif menuChoice == "6" :
        days = input("\nType in how many days you wish to go back:\n")
        history(days)
    elif menuChoice == "7" :
        print("Exiting...")
    else :
        print("This is not a valid input. Please try again")
        menu()

def main() :
    """Display initial welcome message to user, spawn menu()
    """    
    print('\nHello, welcome to COVID-19 spread statistics program!\n')
    menu()

if __name__ == "__main__" :
    main()