import csv
# Function importing data from CSV file
def data_from_csv(countries_dict, country_number, country_number_counter):
    with open("data/countries_data.csv", "r") as file:
        csv_data = csv.reader(file)
        for row in csv_data:
            #Assigning each row item to a specific category
            country, capital, continent, code = row
            #Creating Python dictionary with this data
            countries_dict[country] = {
                "capital": capital, "continent": continent, "code": code}
            #Assigning country to number
            country_number[country_number_counter] = country
            country_number_counter += 1