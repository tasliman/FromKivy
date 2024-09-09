from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window

# from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
import ggwave
import pyaudio
import requests


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        box_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 0.15))
        box_layout.pos_hint={'center_x': .5, 'center_y': .5}

        grid_layout = GridLayout(cols=2)
        label = Label(text="Username:", font_size='15')
        grid_layout.add_widget(label)
        self.username_input = TextInput(multiline=False, font_size='15')
        grid_layout.add_widget(self.username_input)

        label = Label(text="PassWord:", font_size='15')
        grid_layout.add_widget(label)
        self.password_input = TextInput(multiline=False, font_size='15')
        grid_layout.add_widget(self.password_input)

        box_layout.add_widget(grid_layout)

        login_button = Button(text='OK' , size_hint=(1, 0.5), on_press=self.check_login)
        # login_button.bind(on_release=self.dismiss)

        box_layout.add_widget(login_button)

        self.add_widget(box_layout)
        # self.add_widget(ExitButton())

    
    def check_login(self, instance):
        if self.username_input.text == '1' and self.password_input.text == '1':
            app = App.get_running_app()
            app.root.current = 'enter'
        else:
            invalid_popup = Popup(title='Invalid Login', content=Label(text='Invalid username or password'), size_hint=(None, None), size=(250, 100))
            invalid_popup.open()


class EnterScreen(Screen):
    def __init__(self, **kwargs):
        super(EnterScreen, self).__init__(**kwargs)
        box_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 0.25))
        box_layout.pos_hint={'center_x': .5, 'center_y': .5}

        grid_layout = GridLayout(cols=1)
        self.send_text = TextInput(multiline=False, font_size='20', size_hint=(1, 0.25))
        grid_layout.add_widget(self.send_text)

        send_button = Button(text='Send' , size_hint=(1, 0.25), on_press=self.sendmessage)
        grid_layout.add_widget(send_button)

        repo_button = Button(text='Report' , size_hint=(1, 0.25), on_press=self.repo_message)
        grid_layout.add_widget(repo_button)

        exit_button = Button(text='Exit' , size_hint=(1, 0.25), on_press=self.exit_app)
        grid_layout.add_widget(exit_button)

        box_layout.add_widget(grid_layout)

        self.add_widget(box_layout)

    def exit_app(self, instance):
        App.get_running_app().stop()

    
    def sendmessage(self, instance):
        p = pyaudio.PyAudio()
        waveform = ggwave.encode(self.send_text.text, protocolId = 1, volume = 20)
        print("Transmitting text " + self.send_text.text + " ...")
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
        stream.write(waveform, len(waveform)//4)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    def repo_message(self, instance):
            app = App.get_running_app()
            app.root.current = 'send'
        
        
    #     self.add_widget(Button(text='Enter' , size_hint=(.25, 0.05), on_press=self.send_f, pos_hint={'center_x': .5, 'center_y': .5}))

    # def send_f(self, instance):
    #     # print("amir")
    #     p = pyaudio.PyAudio()

    #     # generate audio waveform for string "hello python"
    #     # send_message=input("enter your : ")
    #     send_message= "your : 123456"
    #     waveform = ggwave.encode(send_message, protocolId = 1, volume = 20)

    #     # print("Transmitting text " + send_message + " ...")
    #     stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=1024)
    #     stream.write(waveform, len(waveform)//4)
    #     stream.stop_stream()
    #     stream.close()

    #     p.terminate()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        try:
            responce = requests.get('http://127.0.0.1:8000/todo')
            todos = responce.json()
            # todos = jsonrequest
            for todo in todos:
                print(todo['tarikh_hozur'],todo['saat_hozur'])

            box_layout = BoxLayout(orientation='vertical')

            grid_layout = GridLayout(cols=2)

            for todo in todos:
                # print(todo['tarikh_hozur'],todo['saat_hozur'])
                label = Label(text=todo['tarikh_hozur'], font_size='15')
                grid_layout.add_widget(label)
                self.username_input = TextInput(text=todo['saat_hozur'],multiline=False, font_size='15')
                grid_layout.add_widget(self.username_input)

            box_layout.add_widget(grid_layout)

            self.add_widget(box_layout)
            
        except Exception:
            invalid_popup = Popup(title='Invalid Enternet', content=Label(text='Invalid Enternet, not coonection found!'), size_hint=(None, None), size=(250, 100))
            invalid_popup.open()

class LoginApp(App):
    def build(self):
        Window.size = (400, 600)
        sm = ScreenManager()
        login_screen = LoginScreen(name='login')
        enter_screen =EnterScreen(name='enter')
        # main_screen = MainScreen(name='main')
                
        sm.add_widget(login_screen)
        sm.add_widget(enter_screen)
        # sm.add_widget(main_screen)
        
        return sm


if __name__ == '__main__':
    LoginApp().run()

