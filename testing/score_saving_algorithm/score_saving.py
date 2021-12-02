import csv
from collections import defaultdict

mode_selected = input('''
Select mode:
capitals
flags
continents
''')
score = int(input('''
Write new hiscore
'''))
print(f'Currently selected mode {mode_selected}, score to check: {score}')

#Default dict for storing data from CSV file
columns = defaultdict(list)
with open('test_scores.csv', 'r+') as data:
    reader = csv.DictReader(data)
    for row in reader:
        #Assigning values from each columnt to a list 
        for (column,value) in row.items():
            #Converting numeric values to int for comparison purposes
            if value.isnumeric():
                columns[column].append(int(value))    
            else:
                columns[column].append(value)

#Checking if the new score is higher than others in the file   
for hiscore in range(0,len(columns[mode_selected])):
    if score > columns[mode_selected][hiscore]:
        columns[mode_selected].insert(hiscore,score)
        columns[mode_selected].pop()
        break

#Variable for storing data to be saved in hisscores csv file
output_str = 'capitals,flags,continents\n'

#Add each hiscore value for every mode to ouput_str
for current_score in range(0,10):
    output_str = output_str + str(columns['capitals'][current_score]) + ',' + str(columns['flags'][current_score]) + ',' + str(columns['continents'][current_score]) + '\n'

#Save values to a file
with open('test_scores.csv','w') as data_to_write:
    data_to_write.write(output_str)