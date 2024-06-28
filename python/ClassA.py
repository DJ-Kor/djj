from ClassB import MYCLASS_2
import logging
import os
print('os imported')
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class MYCLASS_1:
    DAYS_PER_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    CLASS_VAR = "CLASS VER 1"

    def __init__(self,):
        print('[2] def __init__(self, _logger) 1')

        self.logger = None
        self.PATH_PREFIX = "/home5/iddx/data/ledbiz"
        self.inst_var = "INITIAL 1"

    def process1(self):
        print('[5] process1() start')
        myc2 = MYCLASS_2()
        print('[9] back to process1() ----')
        vl = ['a', 'abc', '가']
        for v in vl:
            myc2.process2(v)

    def process11(self):
        print('process11()')

        mmyycc = MYCLASS_2()

        test = ['jdj', '김철수']
        for t in test:
            mmyycc.process22(t)
            mmyycc.process222(self.inst_var)


if __name__ == "__main__":
    # logger = common_utils.get_logger(filename=__file__, name=__name__, level=logging.DEBUG)
    print('[1] __name__ == "main__ 1"')

    try:
        app = MYCLASS_1()
        print('[3] app.CLASS_VAR =', app.CLASS_VAR)
        print('[4] app.inst_var =', app.inst_var)
        app.process11()

    except Exception as ex:
        print(ex)