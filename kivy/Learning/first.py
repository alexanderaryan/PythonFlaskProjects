import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class MyGrid(GridLayout):

    def __init__(self,**kwargs):
        super(MyGrid,self).__init__(**kwargs)
        self.cols=1

        self.inside=GridLayout()
        self.inside.cols = 2
        self.inside.add_widget(Label(text="Type a number"))
        self.num1= TextInput(multiline=False)
        self.inside.add_widget(self.num1)

        self.inside.add_widget(Label(text="Type a number"))
        self.num2 = TextInput(multiline=False)
        self.inside.add_widget(self.num2)

        self.add_widget(self.inside)

        self.submit = Button(text="Submit",font_size=30)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def pressed(self,instance):
        print (self.num1.text+self.num2.text)
        print ("pressed")


class MyApp(App):
    def build(self):
        return MyGrid()

MyApp().run()
