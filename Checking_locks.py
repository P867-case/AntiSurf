import json
import signal
import platform
import time

from sqlApi import Api
from datetime import datetime as dt
from multiprocessing import Process



class Proccesing():
    def __init__(self):
        self.api = Api('data.db')
        with open('data/settings.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.start_time = data['start_time']
            self.end_time = data['end_time']
        f.close()

        if platform.system() == 'Linux':
            self.root_path = '/etc/hosts'
        elif platform.system() == 'Windows':
            self.root_path = r'C:\Windows\System32\drivers\etc\hosts'

        self.website_list = []
        for i in self.api.get_all_website():
            self.website_list.append(i[1])
        self.redirect = '127.0.0.1'



    def working_url(self):
        while True:
            ymd = (dt.now().year, dt.now().month, dt.now().day)
            if dt(*ymd, self.start_time) < dt.now() < dt(*ymd, self.end_time):
                print("Доступ ограничен")
                file = open(self.root_path, "r+")
                content = file.read()
                for website in self.website_list:
                    if website in content:
                        pass
                    else:
                        file.write(self.redirect + " " + website + "\n")
            else:
                print("Доступ разрешён")
                file = open(self.root_path, 'r+')
                content = file.readlines()
                file.seek(0)
                for line in content:
                    if not any(website in line for website in self.website_list):
                        file.write(line)
                    file.truncate()
            time.sleep(5)

    def run(self):
        self.www = Process(target=self.working_url)
        self.www.start()


if __name__ == '__main__':
    try:
        proc = Proccesing()
        proc.run()
    except FileNotFoundError:
        print("Запустите файл GUI_SETTINGS_APP.py")
