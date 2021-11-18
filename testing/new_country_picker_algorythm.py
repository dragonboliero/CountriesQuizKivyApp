'''
New algorythm for choosing countries in different modes.
In capitals mode 
'''

import csv
import random

c_dict = {}


#No longer assigning countries to numbers as from now on
#countries will be randomly picked from a list 
#with random.choice() method.
def data_from_csv(countries_dict):
    with open("test_countries_data.csv", "r") as file:
        csv_data = csv.reader(file)
        for row in csv_data:
            #Assigning each row item to a specific category
            country, capital, continent, code = row
            #Creating Python dictionary with this data
            countries_dict[country] = {
                "capital": capital, "continent": continent, "code": code}
    return countries_dict

#Function choosing unique number of countries specified by user
def choose_random_countries(correct_country,countries_list,no_countries_to_choose):
    random_countries = []
    is_different = False
    for country_no in range(0,no_countries_to_choose):
        while is_different == False:
            get_random_country = random.choice(countries_list)

            if get_random_country != correct_country and get_random_country not in random_countries:
                random_countries.append(get_random_country)
                is_different = True
            else:
                is_different = False
        #If we choose unique country is_different needs to be reseted to False
        is_different = False
    return random_countries


c_dict = data_from_csv(c_dict)
current_dict = list(c_dict.keys())
print(f"List of countries before removing anything {current_dict}")

#This algorythm will be used in capitals quiz and continents quiz modes 
#because they require only one country to be chosen from the dictionary
'''
while True:
    #Proceed if there are still countries to choose from 
    if len(current_dict) > 0:
        random_country = random.choice(current_dict)
        print(f"What is the capital of {random_country}?")
        u_input = input()
        #If user provided correct answer then remove country
        #from the list.
        if u_input == c_dict[random_country]["capital"]:
            print("Well done")
            current_dict.remove(random_country)
            print(f"Removing {random_country}")
            print(current_dict)
        #If not leave it in the list
        else:
            print("Wrong answer")
    #If there are no more countries from the list, assign all of them
    #to the list.
    else:
        print("Well done!!! You've guessed all capitals reloading dictionary")
        current_dict = list(c_dict.keys())
'''

#This algorythm will be used in flags quiz which requires four random countries
#at once
while True:

    correct_country = random.choice(current_dict)
    #Normal mode if we have enough countries in the list to fill 4 spaces.
    if len(current_dict) > 3:
        other_countries = choose_random_countries(correct_country,current_dict,3)
        print(f"What is the flag of {correct_country}")
        print(f"{correct_country} , {other_countries[0]} , {other_countries[1]} ,{other_countries[2]}")
        u_input = input()
        
    #'End modes' when user already guessed almost all countries and there are
    #not enough countries to populate 4 spaces.
    elif len(current_dict) == 3:
        other_countries = choose_random_countries(correct_country,current_dict,2)
        print(f"What is the flag of {correct_country}")
        print(f"{correct_country} , {other_countries[0]} , {other_countries[1]}")
        u_input = input()
    elif len(current_dict) == 2:
        other_countries = choose_random_countries(correct_country,current_dict,1)
        print(f"What is the flag of {correct_country}")
        print(f"{correct_country} , {other_countries[0]}")
        u_input = input()
    elif len(current_dict) == 1:
        print(f"What is the flag of {correct_country}")
        print(f"{correct_country}")
        u_input = input()
    
    #If user provided correct answer, remove it from the dictionary
    if u_input == correct_country:
        current_dict.remove(correct_country)
        print(current_dict)
        print("\n")
    
    #If there are only four countries on the list more countries from the list, assign all of them
    #to the list.
    if len(current_dict) == 0:
        print("Well done!!! You've guessed all capitals reloading dictionary")
        current_dict = list(c_dict.keys())
        print(f'Dictionary after reloading{current_dict}')


