
def run():
    print("hello world")

    func('djj', 30, 'college')
    func(1, '30', 'college')

    print('process ends')


def func(name: str, age: int, school=None):
    print('---func', name, age, school)


run()