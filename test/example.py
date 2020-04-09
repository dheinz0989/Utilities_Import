import sys
sys.path.append("../src")
sys.path.append("./src")
from utilities import Decorators, Logger, Dict_to_Obj, ClassAttrHandler


log = Logger.log

log.info('A Logger instance has been created by calling "Logger.log"')

log.info('Continuing with 4 Decorator examples')
log.info(f"\n\n{30*'-'}Decorator 1: run_time.{30*'-'}\nDocu: it indicates the function's run time in a hh:mm:ss after the function returns\nDecorates the function 'foo'")

@Decorators.run_time
def foo(x):
    j = 0
    for i in range(x):
        j +=i
    return j


log.info('Running it with x = 50.000.000\nResult:')
foo(50000000)

log.info(f"\n\n{30*'-'}Decorator 2: show_args.{30*'-'}\n Docu:indicates the arguments passed to the function.\nDecorates the function 'foo'")


@Decorators.show_args
def foo(x):
    j = 0
    for i in range(x):
        j +=i
    return j


log.info('Running it with x = 50.000.000\nResult:')
foo(50000000)


log.info(f"\n\n{30*'-'}Decorator 3: counter.{30*'-'}\n Docu:indicates how often the function has been called.\nDecorates the function 'foo'")
@Decorators.counter
def foo(x):
    j = 0
    for i in range(x):
        j +=i
    return j

log.info('Running the function twice. Result:')
foo(10)
foo(100)

"""
log.info(f"\n\n{30*'-'}Decorator 4: retry.{30*'-'}\n Docu:it tries to execute the function. If the function returns successfully, "
         f"control is passed to the code right after the function. If however, a function fails to return successfully,"
         f" it is called once more until trying to successfully finishing it. This procedure is repeated until the functions "
         f"returns successfully or if it hits the number of limits of retries. Furthermore, the delay parameters adds"
         f" a sleeping time after each try.\nDecorates the erroneously called  function 'foo' with 2 retries and a stalling time of 3 seconds")

@Decorators.retry(2,3)
def foo(x):
    return int(x)

try:
    log.info('Running the function with a wrong argument. Result:')
    foo('Hello World')
except ValueError:
    pass
"""

log.info(f"\n\n{50*'*'}More Decorators are found in the module itself and are not shown in this example.{50*'*'}")

log.info(f"\n\n{30*'-'}Dict_to_Obj{30*'-'}\n Docu:This class constructs an object notation out of a dictionary.")

foo = {
    'a' : 1,
    'b' : 2,
    'c' : 3
}

log.info('The dictionary "foo" is as follows:')
log.info(foo)
log.info('constructing a "Dict_to_Obj" yields:')
foo = Dict_to_Obj(foo)
log.info(foo)
log.info(f'foo.a: {foo.a}, foo.b:{foo.b}, foo.c: {foo.c}')

log.info(f"\n\n{30*'-'}ClassAttrHandler: counter.{30*'-'}\n Docu:This class provides some functionalities with respect to class instance attributes.")


log.info(f'Defining a class Foo with the attributes x, y, z.\nIt inherits the ClassAttHandler class')


class Foo(ClassAttrHandler):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

log.info("Creating an object with with arguments (10,['a','b','c'], '' ")
foo = Foo(10, ['a','b','c'], '')
log.info('As the object is now iterable, we can iterate over it. The first entry is the attribute label whereas the second is the')
for i in foo:
    log.info(i)

log.info('Get a list of all attribute label:')
log.info(foo.attributes_labels)
log.info('And a list of all attributes value')#. Filter them to only get a attributes of type ``int``')
log.info(foo.attributes_values)
log.info('deleting all empty arguements yields:')
foo._delete_empty_attributes()
log.info(foo.attributes_labels, foo.attributes_values)
