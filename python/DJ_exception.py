# Exception & Raise

try:
    import ABC
except ImportError as ex:
    print('import Error')
    print(ImportError)
    print(ex)  # No module named 'ABC'
    print(ex.args)  # ("No module named 'ABC'",)


def process():
    try:
        process2()
    except Exception as ex:
        print(f"process - {ex}")
        raise EOFError('암거나')

    finally:
        print('process - finally')


def process2():
    a = 2
    if a == 2:
        raise Exception('Process2 a==2 exception')

    print('not print after raise')


if __name__ == "__main__":
    try:
        print("__name__ == __main__")
        process()

    except Exception as ex:
        print('except __MAIN__')
        print(ex)