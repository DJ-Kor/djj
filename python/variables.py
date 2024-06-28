import os
print('[1] os imported')

GLO_VAR = "Global Var"
print(GLO_VAR)


class MyClass():
    CLASS_VAR = "Class Var"
    print(CLASS_VAR)

    def __init__(self):
        self.ins_var = "instance var"
        self.client_edl = None
        print(self.ins_var)

    def setup(self):
        self.client_edl = "(setup change client edl)"

    def func1(self):
        print(f'func1 {self.client_edl}')

        self.func2(client_edl=self.client_edl)

    def func2(self, client_edl):
        print(f'func2 {client_edl}')


if __name__ == "__main__":
    print("__name__ == __main__")

    mc_instance = MyClass()

    mc_instance.setup()
    mc_instance.func1()
    mc_instance2 = MyClass()