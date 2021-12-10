import csv
import gspread
from collections import defaultdict

from pyasn1.type.univ import Null

# Function importing data from CSV file.
def data_from_csv(countries_dict, list_of_countries):
    with open("data/countries_data.csv", "r") as file:
        csv_data = csv.reader(file)
        for row in csv_data:
            # Assigning each row item to a specific category.
            country, capital, continent, code = row
            # Creating Python dictionary with this data.
            countries_dict[country] = {
                "capital": capital, "continent": continent, "code": code}
        list_of_countries = list(countries_dict.keys())
        return list_of_countries

#Function for getting user hiscores.
def get_scores():
    hiscores_columns = defaultdict(list)
    with open('data/hiscores.csv', 'r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            # Assigning values from each column to a list.
            for (column, value) in row.items():
                hiscores_columns[column].append(value)
    return hiscores_columns

#Function for getting global hiscores from a remote file.
def get_global_hiscores(username):
    #This function requires a .json file generated in Google Cloud Platform..
    #It connects the script with Google Account.
    #Info how to get it: https://www.youtube.com/watch?v=bu5wXjz2KvU
    service_account = gspread.service_account()
    #Open file with data
    data_base = service_account.open('CQHiscores')

    #Assign spreadsheets to variables.
    capitals_sheet = data_base.worksheet('capitals')
    flags_sheet = data_base.worksheet('flags')
    continents_sheet = data_base.worksheet('continents')

    #Get player names and results from 10 best players in each mode.
    capitals_global_scores = capitals_sheet.get('A1:B10')
    flags_global_scores = flags_sheet.get('A1:B10')
    continents_global_scores = continents_sheet.get('A1:B10')

    #Get user's position from the spreadsheets
    user_capitals = capitals_sheet.find(username)
    user_flags = flags_sheet.find(username)
    user_continents = continents_sheet.find(username)
    
    #Assingn collected data to a dictionary.
    global_scores_dictionary = {}
    global_scores_dictionary["capitals"] = capitals_global_scores
    global_scores_dictionary["flags"] = flags_global_scores
    global_scores_dictionary["continents"] = continents_global_scores
    global_scores_dictionary[username] = []
    if user_capitals == None:
        global_scores_dictionary[username].append({'capitals':'No score yet'})
    else:
        global_scores_dictionary[username].append({'capitals':capitals_sheet.cell(user_capitals.row,user_capitals.col+1).value})
    if user_flags == None:
        global_scores_dictionary[username].append({'flags':'No score yet'})
    else:
        global_scores_dictionary[username].append({'flags':flags_sheet.cell(user_flags.row,user_flags.col+1).value})
    if user_continents == None:
        global_scores_dictionary[username].append({'continents':'No score yet'})
    else:
        global_scores_dictionary[username].append({'continents':continents_sheet.cell(user_continents.row,user_continents.col+1).value})

    print(global_scores_dictionary[username])
    return global_scores_dictionary


get_global_hiscores('Andre')