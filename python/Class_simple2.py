import os
import sys
sys.path.append(os.getcwd())
print('cwd=', os.getcwd())

# import python.Class_simple
from python.Class_simple import MYCLASS_1

if __name__ == "__main__":
    print('★ __main__')

    try:
        my = MYCLASS_1()
        print('★  try')

    except Exception as ex:
        print('★', ex)