
def logging(func):
    import sys
    def _deco():
        try:
            func()
        except Exception as e:
            with open("run.log", "a") as f:
                sys.print_exception(e, f)
    return _deco

@logging
def bar():
    print('this is test output run.log')
    c = e

bar()