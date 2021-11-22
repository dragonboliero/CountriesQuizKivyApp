'''
To do list:
    *Adjust buttons size in main menu, so that all have the same width.
    *Add score multipliers achieved with score streaks.
    *Find icons for categories.
    *Redesign screens. Create a screen template class for quizes screens 
    which will inherit from it.
    *Investigate why images in flags quiz mode don't scale properly on 
     Android.
    *Currently data picker doesn't work in Android build. There's an error
     stating that there is no such module (Need a solutoon).
    *Make the app working in the background.
    *Change algorythm for questions. Instead of constant random vales, remove
    value from dictionary when it was used and place in temporary variable. 
    *Find images of continents outlines for continents quiz mode and adjust
    them to fit them properly in grid tiles.
    *Add animaiton + sound appearing after an answer. (To be considered)

'''

#!/usr/bin/python3
# Module for importing csv files
import csv
# Random numbers generator module
import random

import dataloader as dt

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
#from kivymd.uix.picker import MDThemePicker
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar


# Dictionary with master data about countries
c_dict = {}
#List for performing operations on countries data
countries_list = []
# Dictionary assigning number to each country
c_number = {}
c_number_counter = 0


# Assigning data to appropriate variables
countries_list = dt.data_from_csv(c_dict, c_number, c_number_counter,countries_list)


# This method makes device keyboard appear below main screen
Window.softinput_mode = 'pan'


# ScreenManager and Screen classes
class SManager(ScreenManager):
    pass


class TemplateScreen(Screen):
    test_list = countries_list


class MainMenu(TemplateScreen):
    pass


class Capitals(TemplateScreen):
    pass


class Flags(TemplateScreen):
    pass


class Continents(TemplateScreen):
    pass


class Options(TemplateScreen):
    pass


# Main application class
class CountriesQuiz(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        # Setting up first values of screen variables
        self.score = 0
        self.contry_name = ''
        self.correct_answers = 0
        self.answer_streak = 0
        # Default backgrund RGBA value
        self.bg_color = (78/255, 99/255, 194/255, 1)
        # Loading .kv file
        self.uix = Builder.load_file('uix.kv')
        return self.uix


    '''Method used in all modes for determining country used in current 
       question.(To be modified in the future)
    '''
    def pick_country(self, mode_number):
        
        """ Old function
        country_picker = random.randrange(0, 196)
        self.country_name = c_number[country_picker]
        self.country_chosen = self.country_name
        """
        self.country_name = ""
        #If there are no more countries from the list, assign all of them
        #to the list.
        if len(countries_list) == 0:
            self.reload_countries_list()
        #Proceed if there are still countries to choose from 
        if len(countries_list) > 0:
            self.country_name = random.choice(countries_list)
            print(f"Chosen country: {self.country_name}?")
            print(f"No of countries still in dictionary{len(countries_list)}\n")

        if mode_number == 0:
            self.text_to_display = "What is the capital of {}?".format(
                self.country_name)
            self.root.get_screen(
                'CapitalsScreen').ids.question.text = self.text_to_display

        if mode_number == 2:
            self.text_to_display = "On which continent lies {}?".format(
                self.country_name)
            self.root.get_screen(
                'ContinentsScreen').ids.continent_question.text = self.text_to_display

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
            self.add_canswer()
            self.add_streak(True)
            self.add_points(0)
            self.clear_answer_field()
            '''Testing animation displayed after correct answer, to be
               completed later.
            self.root.get_screen('CapitalsScreen').ids.gif.opacity = 1
            self.root.get_screen('CapitalsScreen').ids.gif.anim_delay = 0.1
            '''
            #Prompt displayed after correct answer
            user_answer = Snackbar(
                text="Congratulations, correct answer.",
                snackbar_x="40dp",
                pos_hint={'center_x': 0.5, 'center_y': 0.4},
                bg_color=(0.2, 1, 0.3, 0.2),
                font_size="15sp").open()

        else:
            print('Wrong answer')
            # Zero correct answer streak
            self.add_streak(False)
            self.clear_answer_field()
            if len(c_dict[self.country_name]['capital']) < 10:
                snack_font_size = "15sp"
            else:
                snack_font_size = "10sp"
            #Prompt displayed after wrong answer
            user_answer = Snackbar(
                text=f"Wrong answer. It's {c_dict[self.country_name]['capital']}.",
                snackbar_x="40dp",
                snackbar_y="40dp",
                pos_hint={'center_x': 0.5, 'center_y': 0.4},
                bg_color=(1, 0, 0, 0.2),
                font_size=snack_font_size).open()


    '''Multi-mode method adding points to user score.The indexing [7:] is 
       present because in each mode score indicator string starts with
       'Score: ', so with 7th index begins current numeric value.Tried to 
       do it as one segment for all modes, but replacing kivy widget id with a 
       variable breaks this function. (To be investigated)
    '''
    def add_points(self, mode_number):
        # Capitals
        if mode_number == 0:
            self.score = int(self.root.get_screen(
                'CapitalsScreen').ids.bot_bar.title[7:]) + 100
            score_text = 'Score: {}'.format(self.score)
            self.root.get_screen(
                'CapitalsScreen').ids.bot_bar.title = score_text
        # Flags
        if mode_number == 1:
            self.score = int(self.root.get_screen(
                'FlagsScreen').ids.flag_score.text[7:]) + 100
            score_text = 'Score: {}'.format(self.score)
            self.root.get_screen(
                'FlagsScreen').ids.flag_score.text = score_text
        # Continents
        if mode_number == 2:
            self.score = int(self.root.get_screen(
                'ContinentsScreen').ids.conti_score.text[7:]) + 100
            score_text = 'Score: {}'.format(self.score)
            self.root.get_screen(
                'ContinentsScreen').ids.conti_score.text = score_text


    # Used only in capiatals quiz mode
    def clear_answer_field(self):
        self.root.get_screen('CapitalsScreen').ids.answer.text = ''


    '''Used only in capitals quiz mode. Increments number of correct user
       answers and displays them in appropriate kivy widget. The indexing
       is based on the same principle as in add_points method, but here 
       score preceding text is: 'Correct answers: '
    '''
    def add_canswer(self):
        self.correct_answers = int(self.root.get_screen(
            'CapitalsScreen').ids.correct_answers.text[17:]) + 1
        current_canswers = self.root.get_screen(
            'CapitalsScreen').ids.correct_answers.text[:17] + str(self.correct_answers)
        self.root.get_screen(
            'CapitalsScreen').ids.correct_answers.text = current_canswers


    '''Used only in capitals quiz mode. Increases correct answers streak or
       resets it if the answer is incorrect. The indexing
       is based on the same principle as in add_points method, but here 
       score preceding text is: 'Current streak: '
    '''
    def add_streak(self, correct_or_wrong):
        if (correct_or_wrong):
            self.answer_streak = int(self.root.get_screen(
                'CapitalsScreen').ids.ca_streak.text[15:]) + 1
            current_answer_streak = self.root.get_screen(
                'CapitalsScreen').ids.ca_streak.text[:16] + str(self.answer_streak)
            self.root.get_screen(
                'CapitalsScreen').ids.ca_streak.text = current_answer_streak
        else:
            self.root.get_screen(
                'CapitalsScreen').ids.ca_streak.text = 'Current streak: 0'


    # Used only in flags quiz mode.
    def pick_flag(self):
        country_picker = random.randrange(0, 196)
        self.flag_name = c_number[country_picker]
        self.flag_chosen = self.flag_name
        self.text_to_display = "What is the flag of {}?".format(
            self.flag_name)
        self.root.get_screen(
            'FlagsScreen').ids.what_country_flag.text = self.text_to_display
        # Randomly pick a place where flag with correct answer will be placed
        correct_flag_place = random.randrange(0, 4)
        # Array holding all items displaying flags in this mode
        self.flag_position = [self.root.get_screen(
            'FlagsScreen').ids.country0, self.root.get_screen(
            'FlagsScreen').ids.country1, self.root.get_screen(
            'FlagsScreen').ids.country2,
            self.root.get_screen(
            'FlagsScreen').ids.country3]

        # Assigning flag images to appropriate kivy widget
        for i in range(0, 4):

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
                random_flag = c_number[random.randrange(0, 196)]
                cf_path = 'data/flags/{}_flag-jpg-xs.jpg'.format(
                    random_flag.lower().replace(' ', '-'))
                self.flag_position[i].source = cf_path

        return self.flag_chosen


    '''Used only in flags quiz mode. Indice ranges are explained in 
       description of add_canswer and add_streak methods.'''
    def check_flag(self, image_number):
        flag_clicked = self.jpg_file_name_to_country_name(image_number)

        if flag_clicked == self.flag_chosen.lower():
            print('good answer')
            add_ca = int(self.root.get_screen(
                'FlagsScreen').ids.flag_ca.text[17:]) + 1
            self.root.get_screen('FlagsScreen').ids.flag_ca.text = self.root.get_screen(
                'FlagsScreen').ids.flag_ca.text[:17] + str(add_ca)

            add_streak = int(self.root.get_screen(
                'FlagsScreen').ids.flag_streak.text[15:]) + 1
            self.root.get_screen('FlagsScreen').ids.flag_streak.text = self.root.get_screen(
                'FlagsScreen').ids.flag_streak.text[:15] + str(add_streak)
            print(add_ca)
            self.add_points(1)
        else:
            print('wrong answer')
            self.root.get_screen('FlagsScreen').ids.flag_streak.text = self.root.get_screen(
                'FlagsScreen').ids.flag_streak.text[:15] + '0'
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
            'ContinentsScreen').ids.continent_question.text
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
                'ContinentsScreen').ids.conti_correct.text[17:]) + 1
            self.root.get_screen('ContinentsScreen').ids.conti_correct.text = self.root.get_screen(
                'ContinentsScreen').ids.conti_correct.text[:17] + str(correct_answers)
            #Remove country from current list of countries
            countries_list.remove(self.country_name)
            '''
            Adding +1 to current streak in continents screen. [16:] is the text with space
            the rest is current score number
            '''
            current_streak = int(self.root.get_screen(
                'ContinentsScreen').ids.conti_streak.text[16:]) + 1
            self.root.get_screen('ContinentsScreen').ids.conti_streak.text = self.root.get_screen(
                'ContinentsScreen').ids.conti_streak.text[:16] + str(current_streak)
            print('correct')
        else:
            self.root.get_screen(
                'ContinentsScreen').ids.conti_streak.text = 'Current streak: 0'
            print('false')


    # Widget created when entering theme settings screen
    def color_picker(self):
        #c_picker = MDThemePicker(size_hint=(1,1), on_dismiss = self.go_to_main)
        # c_picker.open()
        print("Picker isn't working at the moment")


    # Method which allows to go back to main menu screen from theme settings
    def go_to_main(self, picker_object):
        self.root.current = 'MainScreen'


    def testing(self):
        print(self.root.get_screen('MainScreen').ids.cq.size[0])


# Running the app
CountriesQuiz().run()
