'''
To do list:
    *Find font that will better fit the app.
    *Make code revision and optimization.

Possible additional features:
    *Online leaderboard with player nicknames and hiscores
    *Translation to other languages.
'''

#!/usr/bin/python3
# Random numbers generator module
import random

#Custom module for loading data needed from files
import dataloader as dt

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog



# Dictionary with master data about countries
c_dict = {}
#List for performing operations on countries data
countries_list = []

# Assigning data to appropriate variables
countries_list = dt.data_from_csv(c_dict, countries_list)


# This method makes device keyboard appear below main screen
Window.softinput_mode = 'pan'
#Resolution which simulates mobile phone
#Window.size = (405,900)


# ScreenManager and Screen classes
class SManager(ScreenManager):
    pass


class TemplateScreen(Screen):
    pass


class MainMenu(TemplateScreen):
    pass


class Capitals(TemplateScreen):
    pass


class Flags(TemplateScreen):
    pass


class Continents(TemplateScreen):
    pass


class HiScores(TemplateScreen):
    pass



# Main application class
class CountriesQuiz(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        # Setting up first values of screen variables
        self.score = 0
        self.country_name = ''
        self.correct_answers = 0
        self.answer_streak = 0
        # Default backgrund RGBA value. Used in kv file
        self.bg_color = (78/255, 99/255, 194/255, 1)
        # Loading .kv file
        self.uix = Builder.load_file('uix.kv')
        return self.uix


    '''Method used in all modes for determining country used in current 
       question.
    '''
    def pick_country(self):

        self.country_name = ""
        #If there are no more countries from the list, assign all of them
        #to the list.
        if len(countries_list) == 0:
            self.reload_countries_list()
        #Proceed if there are still countries to choose from 
        if len(countries_list) > 0:
            self.country_name = random.choice(countries_list)
            print(f"Chosen country: {self.country_name}")
            print(f"No of countries still in dictionary {len(countries_list)}\n")

        return self.country_name


    '''Method used to assign chosen country to question label in capitals 
       and continents quiz modes.
    '''
    def assign_country_to_label(self, mode_number):
        self.country_name = self.pick_country()
        if mode_number == 0:
            self.text_to_display = "What is the capital of {}?".format(
                self.country_name)
            self.root.get_screen(
                'CapitalsScreen').ids.capitals_toolbar.question = self.text_to_display

        if mode_number == 2:
            self.text_to_display = "In which continent lies {}?".format(
                self.country_name)
            self.root.get_screen(
                'ContinentsScreen').ids.continents_toolbar.question = self.text_to_display

        return self.country_name

    #Reloads modified list of countries to original state
    def reload_countries_list(self):
        print("There are no more countries to guess. Loading the list anew.")
        countries_list.clear()
        for i in c_dict.keys():
            countries_list.append(i)
        print(f"List length after reloading: {len(countries_list)}\n")
        return countries_list


    # Method for checking answer in capitals quiz mode
    def check_answer(self):
        if self.root.get_screen('CapitalsScreen').ids.answer.text == c_dict[self.country_name]['capital']:
            print('Well done')
            #Remove country from current list of countries
            countries_list.remove(self.country_name)
            # Add +1 to correct answers, correct answers streak, points and
            # clear answer field
            self.add_points(0)
            self.add_canswer()
            self.add_streak(True)
            self.clear_answer_field()
            #Prompt displayed after correct answer
            self.root.get_screen('CapitalsScreen').ids.answer_popup.text = "[color=#f7faf8]Congratulations, correct answer.[/color]"
            self.root.get_screen('CapitalsScreen').ids.answer_popup.opacity = 1
            self.root.get_screen('CapitalsScreen').ids.answer_popup.md_bg_color = [55/256,209/255,21/255,1]

        else:
            print('Wrong answer')
            # Zero correct answer streak
            self.add_streak(False)
            self.clear_answer_field()
            #Prompt displayed after wrong answer
            self.root.get_screen('CapitalsScreen').ids.answer_popup.text = f"[color=#f7faf8]Wrong answer. The capital of {self.country_name} is {c_dict[self.country_name]['capital']}.[/color]"
            self.root.get_screen('CapitalsScreen').ids.answer_popup.opacity = 1
            self.root.get_screen('CapitalsScreen').ids.answer_popup.md_bg_color = [219/256,20/255,20/255,1]
            


    '''Multi-mode method adding points to user score.The indexing [7:] is 
       present because in each mode score indicator string starts with
       'Score: ', so with 7th index begins current numeric value.Tried to 
       do it as one segment for all modes, but replacing kivy widget id with a 
       variable breaks this function. (To be investigated)
    '''
    def add_points(self, mode_number):
        points_to_add = 10
        streak_modifier = 10
        # Capitals
        if mode_number == 0:
            #Calculates score multiplier based on current streak
            points_to_add += (streak_modifier * int(self.root.get_screen
                ('CapitalsScreen').ids.capitals_toolbar.streak[15:]))
            self.score = int(self.root.get_screen(
                'CapitalsScreen').ids.capitals_toolbar.score[7:]) + points_to_add
            score_text = 'Score: {}'.format(self.score)
            self.root.get_screen(
                'CapitalsScreen').ids.capitals_toolbar.score = score_text
        # Flags
        if mode_number == 1:
            #Calculates score multiplier based on current streak
            points_to_add += (streak_modifier * int(self.root.get_screen(
                'FlagsScreen').ids.flag_toolbar.streak[15:]))
            self.score = int(self.root.get_screen(
                'FlagsScreen').ids.flag_toolbar.score[7:]) + points_to_add
            score_text = 'Score: {}'.format(self.score)
            self.root.get_screen(
                'FlagsScreen').ids.flag_toolbar.score = score_text
        # Continents
        if mode_number == 2:
            #Calculates score multiplier based on current streak
            points_to_add += (streak_modifier * int(self.root.get_screen(
                'ContinentsScreen').ids.continents_toolbar.streak[16:]))
            self.score = int(self.root.get_screen(
                'ContinentsScreen').ids.continents_toolbar.score[7:]) + points_to_add
            score_text = 'Score: {}'.format(self.score)
            self.root.get_screen(
                'ContinentsScreen').ids.continents_toolbar.score = score_text


    # Used only in capiatals quiz mode
    def clear_answer_field(self):
        self.root.get_screen('CapitalsScreen').ids.answer.text = ''
    
    def disable_answer_popup(self):
        self.root.get_screen('CapitalsScreen').ids.answer_popup.opacity = 0


    '''Used only in capitals quiz mode. Increments number of correct user
       answers and displays them in appropriate kivy widget. The indexing
       is based on the same principle as in add_points method, but here 
       score preceding text is: 'Correct answers: '
    '''
    def add_canswer(self):
        self.correct_answers = int(self.root.get_screen(
            'CapitalsScreen').ids.capitals_toolbar.correct_answers[17:]) + 1
        current_canswers = self.root.get_screen(
            'CapitalsScreen').ids.capitals_toolbar.correct_answers[:17] + str(self.correct_answers)
        self.root.get_screen(
            'CapitalsScreen').ids.capitals_toolbar.correct_answers = current_canswers


    '''Used only in capitals quiz mode. Increases correct answers streak or
       resets it if the answer is incorrect. The indexing
       is based on the same principle as in add_points method, but here 
       score preceding text is: 'Current streak: '
    '''
    def add_streak(self, correct_or_wrong):
        if (correct_or_wrong):
            self.answer_streak = int(self.root.get_screen(
                'CapitalsScreen').ids.capitals_toolbar.streak[15:]) + 1
            current_answer_streak = self.root.get_screen(
                'CapitalsScreen').ids.capitals_toolbar.streak[:16] + str(self.answer_streak)
            self.root.get_screen(
                'CapitalsScreen').ids.capitals_toolbar.streak = current_answer_streak
        else:
            self.root.get_screen(
                'CapitalsScreen').ids.capitals_toolbar.streak = 'Current streak: 0'


    '''Used only in capitals quiz mode. Creates file name base on question text.
       Then the file name is used to display a flag of an asked country.
    '''
    def assign_flag(self):
        compatible_name = self.country_name.lower().replace(' ','-')
        flag_file_name = 'data/flags/' + compatible_name + '_flag-jpg-xs.jpg'
        print(flag_file_name)
        self.root.get_screen('CapitalsScreen').ids.question_flag.source = flag_file_name


    # Used only in flags quiz mode.
    def pick_flag(self):
        self.flag_name = self.pick_country()
        self.flag_chosen = self.flag_name
        self.text_to_display = "What is the flag of {}?".format(
            self.flag_name)
        self.root.get_screen(
            'FlagsScreen').ids.flag_toolbar.question = self.text_to_display
        # Array holding all items displaying flags in this mode
        self.flag_position = [self.root.get_screen(
            'FlagsScreen').ids.country0, self.root.get_screen(
            'FlagsScreen').ids.country1, self.root.get_screen(
            'FlagsScreen').ids.country2,
            self.root.get_screen(
            'FlagsScreen').ids.country3]        
        #Check how many countries are available and randomize appropriate
        #number of countries.
        countries_in_the_list = len(countries_list)
        print(f"Total number of countries in the list {countries_in_the_list}")
        countries_to_randomize = 0
        if countries_in_the_list > 3:
            countries_to_randomize = 3
        elif countries_in_the_list == 3:
            countries_to_randomize = 2
            self.root.get_screen(
            'FlagsScreen').ids.country3.opacity = 0
        elif countries_in_the_list == 2:
            countries_to_randomize = 1
            self.root.get_screen(
            'FlagsScreen').ids.country2.opacity = 0
        elif countries_in_the_list == 1:
            countries_to_randomize = 0
            self.root.get_screen(
            'FlagsScreen').ids.country1.opacity = 0
        #Make all flags visible again after reloading countries list
        if countries_in_the_list == len(c_dict.keys()):
            self.root.get_screen(
            'FlagsScreen').ids.country1.opacity = 1
            self.root.get_screen(
            'FlagsScreen').ids.country2.opacity = 1
            self.root.get_screen(
            'FlagsScreen').ids.country3.opacity = 1                                    
        # Randomly pick a place where flag with correct answer will be placed
        correct_flag_place = random.randrange(0, countries_to_randomize+1)
        #List storing chosen countries
        chosen_countries = []
        chosen_countries.append(self.flag_name)
        # Assigning flag images to appropriate kivy widget
        for i in range(0, countries_to_randomize+1):
            # Correct answer flag
            if i == correct_flag_place:
                cf_path = 'data/flags/{}_flag-jpg-xs.jpg'.format(
                    self.flag_name.lower().replace(' ', '-'))
                self.flag_position[i].source = cf_path
            # Other flags
            else:
                '''Choose random flag for other widgets. However, currently
                   flags may overlap as they are no removed from 
                   the list after being used. 
                '''
                random_flag = self.pick_country()
                while random_flag in chosen_countries:
                    random_flag = self.pick_country()
                chosen_countries.append(random_flag)
                cf_path = 'data/flags/{}_flag-jpg-xs.jpg'.format(
                    random_flag.lower().replace(' ', '-'))
                self.flag_position[i].source = cf_path

        print(f'Countries on the list: {chosen_countries}')
        #clear the list before ending the method        
        chosen_countries.clear()
        return self.flag_chosen


    '''Used only in flags quiz mode. Indice ranges are explained in 
       description of add_canswer and add_streak methods.'''
    def check_flag(self, image_number):
        flag_clicked = self.jpg_file_name_to_country_name(image_number)

        if flag_clicked == self.flag_chosen.lower():
            print('good answer')
            print(f"removing {self.flag_chosen} from the list")
            countries_list.remove(self.flag_chosen)
            self.add_points(1)
            add_ca = int(self.root.get_screen(
                'FlagsScreen').ids.flag_toolbar.correct_answers[17:]) + 1
            self.root.get_screen('FlagsScreen').ids.flag_toolbar.correct_answers = self.root.get_screen(
                'FlagsScreen').ids.flag_toolbar.correct_answers[:17] + str(add_ca)

            add_streak = int(self.root.get_screen(
                'FlagsScreen').ids.flag_toolbar.streak[15:]) + 1
            self.root.get_screen('FlagsScreen').ids.flag_toolbar.streak = self.root.get_screen(
                'FlagsScreen').ids.flag_toolbar.streak[:15] + str(add_streak)
            print(add_ca)
        else:
            print('wrong answer')
            self.root.get_screen('FlagsScreen').ids.flag_toolbar.streak = self.root.get_screen(
                'FlagsScreen').ids.flag_toolbar.streak[:15] + '0'
        self.pick_flag()


    '''Used only in flags quiz mode. Converts currently displayed flags
       file paths to country names
    '''
    def jpg_file_name_to_country_name(self, image_number):
        images_array = [self.root.get_screen(
            'FlagsScreen').ids.country0.source, self.root.get_screen(
            'FlagsScreen').ids.country1.source, self.root.get_screen(
            'FlagsScreen').ids.country2.source, self.root.get_screen(
            'FlagsScreen').ids.country3.source]
        clicked_flag_country_name = images_array[image_number]
        clicked_flag_country_name = clicked_flag_country_name.split('/')
        # Currently: 0 - data, 1 - flags, 2 - flag file name
        clicked_flag_country_name = clicked_flag_country_name[2]
        # Another split used to remove the rest of the file name from country name
        clicked_flag_country_name = clicked_flag_country_name.split('_')
        '''File names have hyphen if a country name consists of 2 or more
           parts. So it needs to be replaced with a space.
        '''
        clicked_flag_country_name = clicked_flag_country_name[0].replace(
            '-', ' ')
        print(clicked_flag_country_name)

        return clicked_flag_country_name


    '''Used only in continents quiz. Index range of current_country is 
       [24:-1] becasue first 24 characters in the text of quiestion widget 
       are: 'On which continent lies ', and the rest of the text contains 
       country name.
    '''
    def check_continent(self, image_number):
        current_country = self.root.get_screen(
            'ContinentsScreen').ids.continents_toolbar.question
        current_country = current_country[24:-1]

        if image_number == 0:
            clicked_continent = self.root.get_screen(
                'ContinentsScreen').ids.africa.source
        if image_number == 1:
            clicked_continent = self.root.get_screen(
                'ContinentsScreen').ids.asia.source
        if image_number == 2:
            clicked_continent = self.root.get_screen(
                'ContinentsScreen').ids.europe.source
        if image_number == 3:
            clicked_continent = self.root.get_screen(
                'ContinentsScreen').ids.na.source
        if image_number == 4:
            clicked_continent = self.root.get_screen(
                'ContinentsScreen').ids.oceania.source
        if image_number == 5:
            clicked_continent = self.root.get_screen(
                'ContinentsScreen').ids.sa.source
        '''Index is based continent image path currently 
           'data/continents/continent.jpg'. Fitst 16 are for the path and -4 for
           file extension
        '''
        clicked_continent = clicked_continent[16:-4]

        if c_dict[current_country]['continent'] == clicked_continent:
            # Adding points in continents screen
            self.add_points(2)
            '''
            Adding +1 to correct answers in continents screen. [17:] is the text with space
            the rest is current score number.
            '''
            correct_answers = int(self.root.get_screen(
                'ContinentsScreen').ids.continents_toolbar.correct_answers[17:]) + 1
            self.root.get_screen('ContinentsScreen').ids.continents_toolbar.correct_answers = self.root.get_screen(
                'ContinentsScreen').ids.continents_toolbar.correct_answers[:17] + str(correct_answers)
            #Remove country from current list of countries
            countries_list.remove(self.country_name)
            '''
            Adding +1 to current streak in continents screen. [16:] is the text with space
            the rest is current score number
            '''
            current_streak = int(self.root.get_screen(
                'ContinentsScreen').ids.continents_toolbar.streak[16:]) + 1
            self.root.get_screen('ContinentsScreen').ids.continents_toolbar.streak = self.root.get_screen(
                'ContinentsScreen').ids.continents_toolbar.streak[:16] + str(current_streak)
            print('correct')
        else:
            self.root.get_screen(
                'ContinentsScreen').ids.continents_toolbar.streak = 'Current streak: 0'
            print('false')


    def check_if_hiscore(self,mode,user_score):
        #Load hiscores from the csv file
        current_scores = dt.get_scores()
        #Store new hiscore position on the list
        positon = 0 
        #Check if the current user score is higher than
        #any score in hiscores file.
        for hiscore in range(0,len(current_scores[mode])):
            if int(user_score) > int(current_scores[mode][hiscore]):
                position = hiscore+1
                #Add score in current place
                current_scores[mode].insert(hiscore,user_score)
                #Remove last element from the list of hiscores for 
                #this mode.
                current_scores[mode].pop()
                #Stop searching.
                output_str = 'capitals,flags,continents\n'
                #Save new score to file
                for current_score in range(0,10):
                    output_str = output_str + str(current_scores['capitals'][current_score]) + ',' + str(current_scores['flags'][current_score]) + ',' + str(current_scores['continents'][current_score]) + '\n'
                with open('data/hiscores.csv','w') as data_to_write:
                    data_to_write.write(output_str)
                #Assign different position ending depending on which position the new
                # hiscore will be assigned.   
                score_endings = ['st','nd','rd','th']
                ending = ''
                if position == 1:
                    ending = score_endings[0]  
                elif position == 2:
                    ending = score_endings[1]
                elif position == 3:
                    ending = score_endings[2]
                else:
                    ending = score_endings[3]

                inform_about_new_hiscore = MDDialog(
                    text = f"Congratulations [color=#13D152]{user_score} pts[/color] is a [color=#13D152]new high score[/color]\n and [color=#13D152]{position}{ending}[/color] best score in {mode.capitalize()} mode",
                    radius=[20,20,20,20],
                    #md_bg_color = (19/255,209/255,82/255,1)
                )
                inform_about_new_hiscore.open()
                #break from the loop
                break

    def fill_hiscores(self):
        #Load hiscores from the csv file
        current_scores = dt.get_scores()
        #Fill hiscores in capitals hiscores table
        self.root.get_screen('HSScreen').ids.ca_pos1.text = current_scores['capitals'][0]
        self.root.get_screen('HSScreen').ids.ca_pos2.text = current_scores['capitals'][1]
        self.root.get_screen('HSScreen').ids.ca_pos3.text = current_scores['capitals'][2]
        self.root.get_screen('HSScreen').ids.ca_pos4.text = current_scores['capitals'][3]
        self.root.get_screen('HSScreen').ids.ca_pos5.text = current_scores['capitals'][4]
        self.root.get_screen('HSScreen').ids.ca_pos6.text = current_scores['capitals'][5]
        self.root.get_screen('HSScreen').ids.ca_pos7.text = current_scores['capitals'][6]
        self.root.get_screen('HSScreen').ids.ca_pos8.text = current_scores['capitals'][7]
        self.root.get_screen('HSScreen').ids.ca_pos9.text = current_scores['capitals'][8]
        self.root.get_screen('HSScreen').ids.ca_pos10.text = current_scores['capitals'][9]
        #Fill hiscores in flags hiscores table
        self.root.get_screen('HSScreen').ids.f_pos1.text = current_scores['flags'][0]
        self.root.get_screen('HSScreen').ids.f_pos2.text = current_scores['flags'][1]
        self.root.get_screen('HSScreen').ids.f_pos3.text = current_scores['flags'][2]
        self.root.get_screen('HSScreen').ids.f_pos4.text = current_scores['flags'][3]
        self.root.get_screen('HSScreen').ids.f_pos5.text = current_scores['flags'][4]
        self.root.get_screen('HSScreen').ids.f_pos6.text = current_scores['flags'][5]
        self.root.get_screen('HSScreen').ids.f_pos7.text = current_scores['flags'][6]
        self.root.get_screen('HSScreen').ids.f_pos8.text = current_scores['flags'][7]
        self.root.get_screen('HSScreen').ids.f_pos9.text = current_scores['flags'][8]
        self.root.get_screen('HSScreen').ids.f_pos10.text = current_scores['flags'][9]
        #Fill hiscores in continents table
        self.root.get_screen('HSScreen').ids.co_pos1.text = current_scores['continents'][0]
        self.root.get_screen('HSScreen').ids.co_pos2.text = current_scores['continents'][1]
        self.root.get_screen('HSScreen').ids.co_pos3.text = current_scores['continents'][2]
        self.root.get_screen('HSScreen').ids.co_pos4.text = current_scores['continents'][3]
        self.root.get_screen('HSScreen').ids.co_pos5.text = current_scores['continents'][4]
        self.root.get_screen('HSScreen').ids.co_pos6.text = current_scores['continents'][5]
        self.root.get_screen('HSScreen').ids.co_pos7.text = current_scores['continents'][6]
        self.root.get_screen('HSScreen').ids.co_pos8.text = current_scores['continents'][7]
        self.root.get_screen('HSScreen').ids.co_pos9.text = current_scores['continents'][8]
        self.root.get_screen('HSScreen').ids.co_pos10.text = current_scores['continents'][9]


    def testing(self):
        print("testing")
        

# Running the app
CountriesQuiz().run()

