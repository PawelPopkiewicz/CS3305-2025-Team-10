class A:

    def __init(self):
        self.x = 4

def f(func):
    def wrapper(*args, **kwargs):
        a = A()
        args = tuple(list(args)+[a])
        result = func(*args, **kwargs)
        return result
    return wrapper

@f
def print4(*args):
    print("printing")
    print(a.x)

print4()
