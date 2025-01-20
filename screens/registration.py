from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.fitimage import FitImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDFillRoundFlatIconButton, MDIconButton



class Registration(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.api = kwargs['sqlapi']
        self.change_func = kwargs['changeF']
        self.name = 'reg'
        self.box = MDCard(
            size_hint=[.7, .7],
            orientation='vertical'
        )
        self.add_widget(MDAnchorLayout(self.box))
        self.box.add_widget(
            MDLabel(
                text='Регистрация',
                font_style='H6',
                halign='center',
                size_hint_y=.2
            )
        )
        self.box.add_widget(MDSeparator())
        self.split_box = MDGridLayout(
            cols=2,
            rows=1
        )
        self.box.add_widget(self.split_box)

        self.left_box = MDBoxLayout(orientation='vertical', padding=[0,40])
        self.logo = FitImage(
            source='data/image/icon.png',
            size_hint=[None, None],
            size=(150,150)
        )
        self.left_box.add_widget(
            MDAnchorLayout(
                self.logo
            )
        )

        self.appname = MDLabel(
            text='AntiSurf',
            font_style='H4',
            halign='center'
        )
        self.left_box.add_widget(self.appname)
        self.description_label = MDLabel(
            text='Давно были проблемы с концентрацией ?\nПриложение AntiSurf поможет вам!',
            halign='center'
        )
        self.left_box.add_widget(self.description_label)
        self.left_box.add_widget(MDBoxLayout())

        self.split_box.add_widget(self.left_box)

        self.right_box = MDBoxLayout(orientation='vertical', padding=[20,0], spacing=20)

        self.right_box.add_widget(MDBoxLayout())

        self.login_text_input = MDTextField(hint_text='Логин', icon_left="account")
        self.right_box.add_widget(self.login_text_input)

        self.box_password = MDBoxLayout()

        self.password_input = MDTextField(hint_text='Пароль', password=True, icon_left="key-variant")
        self.box_password.add_widget(self.password_input)

        self.show_password = MDIconButton(icon='eye-off', on_release=lambda x: self.control_show())
        self.box_password.add_widget(self.show_password)

        self.right_box.add_widget(self.box_password)

        self.right_box.add_widget(
            MDAnchorLayout(
                MDFillRoundFlatIconButton(
                    icon='login',
                    text='Войти в приложение',
                    on_release=lambda x: self.registration()
                )
            )
        )
        self.right_box.add_widget(MDBoxLayout())

        self.split_box.add_widget(self.right_box)

    def control_show(self, *args):
        self.show_password.icon = "eye" if self.show_password.icon == "eye-off" else "eye-off"
        self.password_input.password = False if self.password_input.password is True else True

    def registration(self):
        login = self.login_text_input.text
        password = self.password_input.text
        self.api.create_user(login, password)
        self.change_func()