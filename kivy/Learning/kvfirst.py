import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class MyGrid(Widget):

    num1=ObjectProperty(None)
    num2=ObjectProperty(None)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        print ("touch down",touch)

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        print ("touch up", touch)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        print ("touch move",touch)

    def pressed(self):
        print (self.num1.text+self.num2.text)
        print ("pressed")


class MyApp(App):
    def build(self):
        return MyGrid()

MyApp().run()
