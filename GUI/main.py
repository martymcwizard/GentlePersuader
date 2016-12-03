from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty

import json, os

def on_enter(instance):
    print('User pressed enter in', instance.text)      
    
def on_text(instance, value):
    print('The widget', instance, 'have:', value)

class GUI(Widget):
    topic_menu = ObjectProperty(None)
    persuadee_count = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.addTopicDropDown()
        self.addPersuadeeCount()
        #self.topic_menu = TopicDropDown().menu
        #self.add_widget(self.topic_menu)


    def addTopicDropDown(self):
        # Make sure config.json exists        
        if(os.path.isfile("config.json")):
            with open("config.json") as f:
                config_data = json.load(f)
        #TODO: handle what to do when config.json doesn't exist
        else:
            pass

        #mainbutton = Button(text='Topics', size_hint=(None, None))   
       
        dropdown = DropDown()
        for topic in config_data[0]["topics"]:
            # when adding widgets, we need to specify the height manually (disabling
            # the size_hint_y) so the dropdown can calculate the area it needs.
            btn = Button(text=topic, size_hint_y=None, height=44)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))

            # then add the button inside the dropdown
            dropdown.add_widget(btn)   

        self.topic_menu.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.topic_menu, 'text', x))
    
    def addPersuadeeCount(self):
        self.persuadee_count.multiline=False
        self.persuadee_count.bind(text=on_text)    
        self.persuadee_count.bind(on_text_validate=on_enter)


class GentlePersuaderApp(App):    
    
    def build(self):
        #mainButton = TopicDropDown()
        #return  Button(text='Hello', size_hint=(None, None))
        #return mainButton
        return GUI()

if __name__ == '__main__':
      
    GentlePersuaderApp().run()
