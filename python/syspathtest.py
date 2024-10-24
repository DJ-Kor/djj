import os
import sys
import logging
import syspathtest2
print('●●●●●●●●●●●● sys path test')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + '/../')

print('file의 directory= ', os.path.dirname(__file__))
print('file의 directory (abs)= ', os.path.abspath(os.path.dirname(__file__)))
print('file의 dir의 dir== 하나 상위 dir', os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

print('/../ = >', os.path.pardir)
print('file의 name = ', os.path.basename(__file__))
print(os.path)

print(' sys path test ●●●●●●●●●●●●')


print('--------------------------')
import syspath2.syspath2
print('--------------------------')
import syspath2.syspath3.syspath3
print('--------------------------')