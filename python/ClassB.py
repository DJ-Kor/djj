import logging
import os
import sys
import pandas as pd
import ast
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class MYCLASS_2:
    CCC = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    CLASS_VAR = "CLASS VER 2"

    def __init__(self):
        print('[6] def __init__(self, _logger) 2')

        self.logger = None
        self.PATH_PREFIX = "/home5/iddx/data/ledbiz"
        self.inst_var = "INITIAL 2"
        print('[7] MYCLASS_2.CLASS_VAR =', MYCLASS_2.CLASS_VAR)
        print('[8] self.inst_var =', self.inst_var)

    def process2(self, var):
        print(f" ----- process2(var={var}) ----- ")

        # CLASS VAR
        print("MYCLASS2.CLASS_VAR (1) =", MYCLASS_2.CLASS_VAR)
        self.CLASS_VAR = 'DOES NOT CHANGE'
        print("MYCLASS2.CLASS_VAR (2) =", MYCLASS_2.CLASS_VAR)
        MYCLASS_2.CLASS_VAR = f'THIS WILL CHANGE {var}'
        print("MYCLASS2.CLASS_VAR (3) =", MYCLASS_2.CLASS_VAR)

        # inst_var
        print("self.inst_var (1)", self.inst_var)
        self.inst_var = var
        print("self.inst_var (2)", self.inst_var)

        # global
        global g_var
        g_var = 'G_VAR'
        print(f'g_var = {g_var}')

    def process22(self, df):
        print(f'process22(df = {df})')
        global n_tot
        n_tot = df
        print()

    def process222(self, email_to):
        print(f'process222(email_to = {email_to})')
        # global n_tot
        print(f'n_tot = {n_tot}')
        print(f'MYC1 VAR= ')


if __name__ == "__main__":
    # logger = common_utils.get_logger(filename=__file__, name=__name__, level=logging.DEBUG)
    print('__name__ == "main__" 2')

    try:
        app = MYCLASS_2()
        print('NOT COME HERE')
        print('app.CLASS_VAR', app.CLASS_VAR)
        print('app.inst_var', app.inst_var)

    except Exception as ex:
        print(ex)