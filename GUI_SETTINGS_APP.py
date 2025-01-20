import os
import json
import sqlite3

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window

from screens.control import Index
from screens.registration import Registration
from sqlApi import Api

Window.minimum_height = 580
Window.minimum_width =  900




class Root(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.control_db = Api('')

        self.sm = MDScreenManager()
        self.sm.add_widget(Registration(sqlapi=self.control_db, changeF=self.change))
        self.sm.add_widget(Index(sqlapi=self.control_db))

        self.add_widget(self.sm)

    def change(self):
        self.sm.current = 'index'
        self.sm.screens[1].source_list.add_content_item()
        self.sm.screens[1].JsApi.get_data()
        self.sm.screens[1].set_variable()

class Application(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.root = Root()
        return self.root

    def on_start(self):
        if not os.path.exists('data.db'):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            # Создаем таблицу Source
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Source (
                    id INTEGER PRIMARY KEY,
                    domain TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS User (
                    login TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

            # Сохраняем изменения и закрываем соединение
            connection.commit()
            connection.close()
        self.root.control_db.file = 'data.db'
        self.root.control_db.reconnect()

        if not os.path.exists('data/settings.json'):
            with open('data/settings.json', 'w+') as f:
                f.write(
                    json.dumps(
                        {
                            "appname":"AntiSurf",
                            "start_time":8,
                            'end_time':19
                        },
                        indent=4,
                        ensure_ascii=False
                    )
                )
            f.close()

        if self.root.control_db.get_user() == None:
            self.registration()
        else:
            self.root.sm.current = 'index'
            self.root.sm.screens[1].source_list.add_content_item()
            self.root.sm.screens[1].JsApi.get_data()
            self.root.sm.screens[1].set_variable()

        print(self.root.control_db.get_all_website())

    def registration(self):
        self.root.sm.current = 'reg'

if __name__ == '__main__':
    app = Application()
    app.run()