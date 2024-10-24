import os
import sys


class Parent:
    CLASS_VAR = "CLASS VER - PARENT"

    def __init__(self,):
        print('def __init__(self) ')

        self.logger = None
        self.inst_parent = "Parent Instance Var"
        self.inst_var = "INITIAL 1"

    def __del__(self,):
        print('this is del')
        self.process_parent()

    def process_parent(self):
        print('[5] process_parent() start')


if __name__ == "__main__":
    print('[1] __name__ == "main__ 1"')

    try:
        app = Parent()
        print('[3] app.CLASS_VAR =', app.CLASS_VAR)
        print('[4] app.inst_var =', app.inst_var)
        app.process_parent()

    except Exception as ex:
        print(ex)