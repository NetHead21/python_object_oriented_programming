class A:
    def show_something(slef):
        print("My class is A")


a_object = A()
a_object.show_something()


def patched_show_something():
    print("My class is NOT A")


a_object.show_something = patched_show_something
a_object.show_something()
