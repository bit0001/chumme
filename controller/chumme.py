import os
from os.path import dirname

from kivy.app import App
from kivy.lang import Builder

import iconfonts
from database_manager.util import create_tables_if_not_exist

iconfonts.register('default_font',
                   'resources/fontawesome-webfont.ttf',
                   'resources/font-awesome.fontd')



class ChumMeApp(App):
    def build(self):
        create_tables_if_not_exist()
        return Builder.load_file(
            os.path.join(dirname(__file__), '../view/chumme.kv')
        )
