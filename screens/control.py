import json
import platform


from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import (
    MDFillRoundFlatIconButton, MDFlatButton,
    BaseButton, MDRaisedButton
)


class ApiJs:
    def __init__(self):
        self.file = 'data/settings.json'
        self.data = None

    def get_data(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        f.close()

    def set_data(self):
        with open(self.file, 'w', encoding='utf-8') as f:
            f.write(
                json.dumps(
                    self.data,
                    indent=4,
                    ensure_ascii=False
                )
            )
        f.close()

class RemoveDialog(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.size_hint_y = None
        self.height = 50

        self.textinput = MDTextField(icon_left='form-textbox-password', hint_text='Пароль для удаления')
        self.add_widget(self.textinput)

class ItemWeb(MDBoxLayout, BaseButton):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.size_hint_y = None
        self.height = 50
        self.size_hint_x = 1
        self.api = kwargs['sqlapi']
        self.func = kwargs['reload_func']
        self.url = kwargs['domen']
        self.orientation='vertical'
        self.content_dialog = RemoveDialog()
        self.dialog = MDDialog(
            title='Подтвердите удаление',
            type="custom",
            content_cls=self.content_dialog,
            buttons=[
                MDFlatButton(
                    text="Отмена",
                    theme_text_color="Custom",
                    text_color='#83C5BE',
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="Удалить",
                    theme_text_color="Custom",
                    text_color='#980B1C',
                    on_release=lambda x: self.remove_url()
                ),
            ],

        )

        self.Info = MDLabel(text=self.url)
        self.add_widget(self.Info)
        self.add_widget(MDSeparator())
        self.on_release = lambda: self.dialog.open()

    def remove_url(self):
        password = self.api.get_user()[1]
        if self.content_dialog.textinput.text == password:
            self.api.remove_website(self.url)
            if platform.system() == 'Linux':
                root_path = 'test.txt'
            elif platform.system() == 'Windows':
                root_path = r'C:\Windows\System32\drivers\etc\hosts'

            if 'www' in self.url:
                website_list = [self.url, self.url.replace('www.','')]
            else:
                website_list = [self.url, f'www.{self.url}']

            file = open(root_path, 'r+')
            content = file.readlines()
            file.seek(0)
            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)
                file.truncate()
            file.close()
            self.dialog.dismiss()
            Snackbar(
                text="Адрес удален",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
            self.func()
        else:
            self.dialog.dismiss()
            Snackbar(
                text="Не верный пароль",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()

class ContentInputDialog(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.size_hint_y = None
        self.height = 200

        self.url = MDTextField(icon_left='web',hint_text='url сайта')
        self.add_widget(MDAnchorLayout(self.url))

class ContentInputDialog_two(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.size_hint_y = None
        self.height = 150
        self.orientation = 'vertical'
        self.spacing = 20
        self.s = kwargs['start']
        self.e = kwargs['end']
        self.menu_s = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.press_start_item(x),
            } for i in range(24)
        ]
        self.menu_e = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.press_end_item(x),
            } for i in range(24)
        ]

        self.box_horz = MDBoxLayout(spacing=20)

        self.time_start = MDFillRoundFlatIconButton(
            text=f'Начало в {self.s}:00',
            icon='timer',
            on_release=lambda x:self.menu_viwer_start.open()
        )
        self.box_horz.add_widget(self.time_start)

        self.end_time = MDFillRoundFlatIconButton(
            text=f'Конец в {self.e}:00',
            icon='timer-off',
            on_release=lambda x:self.menu_viwer_end.open()
        )
        self.box_horz.add_widget(self.end_time)
        self.add_widget(
            MDAnchorLayout(
                self.box_horz
            )
        )

        self.menu_viwer_start = MDDropdownMenu(
            caller=self.time_start,
            items=self.menu_s,
            width_mult=4
        )

        self.menu_viwer_end = MDDropdownMenu(
            caller=self.end_time,
            items=self.menu_e,
            width_mult=4
        )

        self.password_input = MDTextField(icon_left='form-textbox-password', hint_text='Пароль для изменения')
        self.add_widget(self.password_input)

    def get_password(self):
        password = self.password_input.text
        self.password_input.text = ''
        return password

    def press_start_item(self, x):
        self.time_start.text = f'Начало в {x}:00'
        self.menu_viwer_start.dismiss()

    def press_end_item(self, x):
        self.end_time.text = f'Конец в {x}:00'
        self.menu_viwer_end.dismiss()

class ScrollViewerSource(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.orientation = 'vertical'
        self.api = kwargs['sqlapi']
        self.dialog = None
        self.data = ContentInputDialog()

        self.info_label = MDLabel(text=kwargs['title'], font_style='H6', size_hint_y=.1, padding=[20,20])
        self.add_widget(self.info_label)
        self.add_widget(MDSeparator())
        self.add_button = MDFillRoundFlatIconButton(icon='plus', text='Добавить сайт', on_release=lambda x: self.open_dialog())
        self.add_widget(
            MDAnchorLayout(
                self.add_button,
                size_hint_y=.1
            )
        )

        self.scroll = MDScrollView()
        self.content = MDBoxLayout(size_hint_y=None, adaptive_height=True, orientation='vertical')
        self.scroll.add_widget(self.content)
        self.add_widget(self.scroll)
        self.init_dialog()

    def add_content_item(self):
        for site in self.api.get_all_website():
            self.content.add_widget(
                ItemWeb(domen=site[1], sqlapi=self.api, reload_func=self.reload)
            )

    def reload(self):
        self.content.clear_widgets()
        self.add_content_item()

    def add_web(self):
        url = self.data.url.text
        self.api.add_website(url)
        self.dialog.dismiss()
        self.reload()
        Snackbar(
            text="Адрес добавлен!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=(
                                Window.width - (dp(10) * 2)
                        ) / Window.width
        ).open()

    def open_dialog(self):
        self.data.url.text = ''
        self.dialog.open()

    def init_dialog(self):
        self.dialog = (
            MDDialog(
                title='Добавление ресурса',
                type="custom",
                content_cls=self.data,
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        theme_text_color="Custom",
                        text_color='#980B1C',
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Добавить",
                        theme_text_color="Custom",
                        text_color='#83C5BE',
                        on_release=lambda x: self.add_web()
                    ),
                ],
            )
        )

class Index(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.name = 'index'
        self.proccesing = False
        self.api = kwargs['sqlapi']
        self.user = 'asd'
        self.JsApi = ApiJs()

        self.box = MDGridLayout(cols=2,rows=1, padding=[20,20])
        self.add_widget(self.box)

        self.left_box = MDBoxLayout(orientation='vertical', size_hint_x=.3)
        self.left_box.add_widget(MDBoxLayout())
        self.username = MDLabel(
            text=self.user,
            font_style='H6',
            halign='center',
            size_hint_y=.2
        )
        self.left_box.add_widget(self.username)

        self.status_processing = MDLabel(
            text=self.get_processing(),
            theme_text_color='Custom',
            text_color='#74C69D',
            font_style='Caption',
            halign='center',
            size_hint_y=.2
        )
        self.left_box.add_widget(self.status_processing)

        self.control_time_box = MDBoxLayout(orientation='vertical')
        self.time_to_block = MDLabel(
            text='',
            halign='center',
            size_hint_y=.1
        )
        self.control_time_box.add_widget(self.time_to_block)
        self.change_time = MDRaisedButton(
            text='Изменить время',
            on_release=lambda x: self.dialog_edit_time.open()
        )
        self.control_time_box.add_widget(
            MDAnchorLayout(
                self.change_time,
            )
        )
        self.left_box.add_widget(self.control_time_box)
        self.left_box.add_widget(MDBoxLayout())

        self.box.add_widget(self.left_box)

        self.right_box = MDBoxLayout(orientation='vertical', spacing=20, padding=[20, 20])

        self.source_list = ScrollViewerSource(title='Блокировать', sqlapi=self.api)
        self.right_box.add_widget(self.source_list)

        self.box.add_widget(self.right_box)


    def save_time(self):
        start = self.content_edit_time.time_start.text.replace("Начало в ", '').replace(':00', '')
        end = self.content_edit_time.end_time.text.replace("Конец в ", '').replace(":00", '')
        if self.api.get_user()[1] == self.content_edit_time.get_password():
            self.dialog_edit_time.dismiss()
            self.JsApi.data['start_time'] = int(start)
            self.JsApi.data['end_time'] = int(end)
            self.JsApi.set_data()
            self.set_variable()
            Snackbar(
                text="Настройки применены",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
        else:
            self.dialog_edit_time.dismiss()
            Snackbar(
                text="Неверный пароль",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()


    def set_variable(self):
        self.user = self.api.get_user()[0]
        self.username.text = self.user
        self.time_to_block.text = f"Время блокировки: \n{self.JsApi.data['start_time']}:00-{self.JsApi.data['end_time']}:00"
        self.JsApi.get_data()

        self.content_edit_time = ContentInputDialog_two(
            start=self.JsApi.data['start_time'],
            end=self.JsApi.data['end_time']
        )

        self.dialog_edit_time = MDDialog(
            title='Изменить время',
            type="custom",
            content_cls=self.content_edit_time,
            buttons=[
                MDFlatButton(
                    text="Отмена",
                    theme_text_color="Custom",
                    text_color='#980B1C',
                    on_release=lambda x: self.dialog_edit_time.dismiss()
                ),
                MDFlatButton(
                    text="Применить",
                    theme_text_color="Custom",
                    text_color='#83C5BE',
                    on_release=lambda x: self.save_time()
                ),
            ],
        )

    def get_processing(self):
        if self.proccesing is True:
            return "Блокировка активна"
        else:
            return "Можно посещать все сайты"
