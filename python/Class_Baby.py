import os
import sys

CUR_FILE_PATH = os.path.abspath(__file__)
print("CUR_FILE_PATH=", CUR_FILE_PATH)
sys.path.append(os.path.dirname(CUR_FILE_PATH))

from Class_Parent import Parent


class Baby(Parent):
    CLASS_BABY = "★ CLASS VER - BABY"

    def __init__(self,):
        print('★ def __init__(self, _logger) 1')

        self.inst_var = " ★ INITIAL BABY"
        Parent.__init__(self)
    
    def __del__(self,):
        print('★ this is del')
                 
    def process_baby(self):
        print('★ process_baby() start')

    def baby_func(self):
        self.process_parent()
        print(self.inst_parent)


if __name__ == "__main__":
    print('★ __name__ == "main__ 1"')

    try:
        app = Baby()
        print('★ app.CLASS_VAR =', app.CLASS_VAR)
        print('★ app.inst_var =', app.inst_var)
        app.baby_func()

    except Exception as ex:
        print(ex)