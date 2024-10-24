import os
print('os imported')
import sys


class MYCLASS_1:
    CLASS_VAR = "CLASS VER 1"

    def __init__(self,):
        print('[2] def __init__(self, _logger) 1')

        self.logger = None
        self.PATH_PREFIX = "/home5/iddx/data/ledbiz"
        self.inst_var = "INITIAL 1"

    def __del__(self,):
        print('this is del')
        self.process1()

    def process1(self):
        print('[5] process1() start')


if __name__ == "__main__":
    print('[1] __name__ == "main__ 1"')

    try:
        app = MYCLASS_1()
        print('[3] app.CLASS_VAR =', app.CLASS_VAR)
        print('[4] app.inst_var =', app.inst_var)
        app.process1()

    except Exception as ex:
        print(ex)