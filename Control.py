# pos project module 03
# Controll system: Controller_abstract

from abc import *

class Control:
    def set_obj(self):
        raise NotImplementedError()

    def search_obj(self):
        raise NotImplementedError()

    def update_obj(self):
        raise NotImplementedError()

    def del_obj(self):
        raise NotImplementedError()