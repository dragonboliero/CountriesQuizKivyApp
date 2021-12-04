import csv
from collections import defaultdict

# Function importing data from CSV file
def data_from_csv(countries_dict, list_of_countries):
    with open("data/countries_data.csv", "r") as file:
        csv_data = csv.reader(file)
        for row in csv_data:
            # Assigning each row item to a specific category
            country, capital, continent, code = row
            # Creating Python dictionary with this data
            countries_dict[country] = {
                "capital": capital, "continent": continent, "code": code}
        list_of_countries = list(countries_dict.keys())
        return list_of_countries


def get_scores():
    hiscores_columns = defaultdict(list)
    with open('data/hiscores.csv', 'r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            # Assigning values from each column to a list
            for (column, value) in row.items():
                hiscores_columns[column].append(value)
    return hiscores_columns
