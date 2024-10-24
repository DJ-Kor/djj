import os
import sys

print('[2] hello ---- sys path test 2 ')


print('[2] ', os.path.basename(__file__))


model_dir = os.path.join('.', 'model_bertopic')

print(model_dir)