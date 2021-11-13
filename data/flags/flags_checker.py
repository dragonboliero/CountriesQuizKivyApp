import csv
from kivymd.app import MDApp
from kivy.lang import Builder

countries_dict = []


mockup = '''
Screen:
    MDLabel:
        id: text_f
        text:'Country: '
        halign: 'center'
        pos_hint:{'center_x':0.5,'center_y':0.6}

    Image:
        id: c_img
        source:''
        pos_hint:{'center_x':0.5,'center_y':0.5}
        size_hint:(0.2,0.15)

    Button:
        text:'Next country'  
        pos_hint:{'center_x':0.5,'center_y':0.2}  
        size_hint:(0.2,0.1)
        on_press: app.switch_image()

'''


with open("C:/Users/Dragonboliero/Dropbox/python mini projekciki/CountriesQuiz/countries_data.csv", "r") as file:
    csv_data = csv.reader(file)

    for row in csv_data:
        country, capital, continent, code = row
        countries_dict.append(country)


class CheckImages(MDApp):
    def build(self):
        self.counter = 181
        print(self.counter)
        program = Builder.load_string(mockup)
        return program

    def switch_image(self):
        self.root.ids.text_f.text = countries_dict[self.counter]
        country_name = countries_dict[self.counter].lower().replace(' ', '-')
        self.root.ids.c_img.source = '{}_flag-jpg-xs.jpg'.format(country_name)
        print(self.counter)
        self.counter += 1


CheckImages().run()
