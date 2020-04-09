'''

This Module provides some Function which are considered util. They are not necessary to run the code but ease it a lot.

In total the following different Utilities classes are provided:
 - Logger: this class initializes a logging instance which can be used to log all activities.
 - Decorators: this class provides a set of different Decorators which can be used to add functionalities to functions
 - ClassAttrHandler: this class provides some functionalities with respect to classes and their respective attributes.
 - Dict_to_Obj: converts a dictionary to an object notation

'''
from os.path import isdir, join
from os import makedirs
import logging
from sys import stdout
from random import random
import time
from functools import wraps

'''
Contains:
- Logger
- Decorator
    - run_time
    - show_args
    - counter
    - retry
    - retry_with_exponential_stalling
    - accepted_args
    - accepted_args_classes
    - accepted_args_type
    - container_non_empty
    - class_has_object
- Dict_to_Obj
- Class Attribute Handler
'''

class Logger:
    """
    This class adds a logging instance which can be imported in other modules and used to track code and activities.
    All logs to are written to stdout and also in a logging file. The logging file is identified via a timestamp and written into ./logs/

    Usage: Import this class at the beginning of a module. You can then access the log attribute and use it as a logging instance
    Example::

    > 1 from Utilities import Logger
    > 2 log = Logger.log
    > 3 log.info('Control is here')
    > # log prints "Control is here"
    """

    if not isdir("logs"):
        makedirs("logs")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d - file: %(module)s  - func: %(funcName)s - line: %(lineno)d - %(levelname)s - msg: %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.FileHandler(
                join(
                    "logs",
                    "log_{0}_{1}".format(
                        __name__, time.strftime("%Y-%m-%d", time.gmtime())
                    ),
                )
            ),
            logging.StreamHandler(stdout),
        ],
    )
    log = logging.getLogger(__name__)

# This module uses a logger itself
log = Logger.log

class Decorators:
    """
    This class provides a set of functionality with respect to decorate functions. These decorators are considered
    util as they prevent to repeat the same code, add functionality to a function on the fly, allows a lot of type
    and input checking and so on.

    All the functions defined inside this class take a function as an input and return a decorated function.
    """

    @staticmethod
    def run_time(func):
        """
        When decorating a function with this decorator, it indicates the function's run time in a hh:mm:ss after
        the function returns.

        Example::

        > # Assume the function needs exactly 1 minute, 13.534 seconds to execute
        > @Decorators.run_time
        > 1 def foo(x):
        > 2   ...
        > ...
        > 7 foo(10)
        > #console prints "00:01:13,534"

        :param func: function to decorate
        :return: decorated function which indicates function run time
        """
        assert callable(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wraps the original function and adds the decorator's run time display functionality
            """
            start = time.time()
            ret = func(*args, **kwargs)
            end = time.time()
            m, s = divmod(end - start, 60)
            h, m = divmod(m, 60)
            ms = int(s % 1 * 1000)
            s, m, h = int(round(s, 0)), int(round(m, 0)), int(round(h, 0))
            log.info(
                f'Execution Time (hh:mm:sec) for function "{func.__name__}": {h:02d}:{m:02d}:{s:02d},{ms:03d}'
            )
            return ret

        return wrapper

    @staticmethod
    def show_args(func):
        '''
        When decorating a function with this decorator, it indicates the arguments passed to the function.

        Example::

        > @Decorators.show_args
        > 1 def foo(x):
        >       ....
        >    10 foo(10)
        >    11 #console prints "Executing 'foo' with args 10 and ''"

        :param func: function to decorate
        :return: decorated function which indicates function's arguments
        '''
        assert callable(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.info(f"Executing '{func.__name__}' with args {args} and {kwargs}")
            ret = func(*args, **kwargs)
            return ret
        return wrapper

    @staticmethod
    def counter(func):
        '''
        When decorating a function with this decorator, it indicates how often the function has been called.

        Example::

         >   @Decorators.counter
         >   1 def foo(x):
         >       ....
         >   10 foo(10)
         >   11 #console prints "Executing 'foo' with args 10 and ''"

        :param func: function to decorate
        :return: decorated function which indicates how often the function has been called
        '''
        assert callable(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.count = wrapper.count + 1
            res = func(*args, **kwargs)
            log.info(f"Number of times '{func.__name__}' has been called: {wrapper.count}x")
            return res
        wrapper.count = 0
        return wrapper

    @staticmethod
    def retry(times, delay):
        """
        When decorating a function with this decorator, it tries to execute the function. If the function returns successfully,
        control is passed to the code right after the function. If however, a function fails to return successfully,
        it is called once more until trying to successfully finishing it. This procedure is repeated until the functions
        returns successfully or if it hits the number of limits of retries. Furthermore, the delay parameters adds
        a sleeping time after each try.

        Target: This decorator is useful for functions which performs requests from/to web applications. For instance, if a server
        is temporarily unreachable, the request is requested in a fixed delay after the first failure.
        Example::

        > @Decorators.retry(5,20)
        > 1 def foo(x):
        >    ...
        > 7 foo(10)
        > # console prints: Trying to execute $foo
        > # upon failure: stalls 20 seconds and tries a next execution after stalling.
        > # after 5 tries, it raises an error

        :param times: how many tries to execute the function
        :type times: int
        :param delay: waiting period between two function calls
        :type delay: int
        :return: a decorated function which tries to execute a specified times and sleeps during two failures. The sleeping amount is a function parameter
        :rtype: func
        """

        def decorator(func):
            """
            Wraps decorator arguments
            """

            @wraps(func)
            def wrapper(*args, **kwargs):
                """
                Wraps the original function and adds the decorator's retry functionality
                """
                t = 1
                while t <= times:
                    try:
                        log.info(f'Trying to execute "{func.__name__}" ({t}/{times})')
                        res = func(*args, **kwargs)
                        log.info(f'Successfully executed "{func.__name__}".')
                        return res
                    except Exception as e:
                        log.warning("Execution failed for the following reason:", e)
                        t += 1
                        if t <= times:
                            time.sleep(delay)
                        else:
                            log.error(
                                f'Function "{func.__name__}" could not be executed after {times} tries'
                            )

            return wrapper

        return decorator

    @staticmethod
    def retry_with_exponential_stalling(times, white_noise=False):
        """
        When decorating a function with this decorator, it tries to execute the function. If the function returns successfully,
        control is passed to the code right after the function. If however, a function fails to return successfully,
        it is called once more until trying to successfully finishing it. This procedure is repeated until the functions
        returns successfully or if it hits the number of limits of retries.
        After each failure of a function, it is stalled (sleeping). The amount of stalling doubles after each unsuccessful try
        which implements and exponential stalling time.

        Target: This decorator is useful for functions which performs requests from the Internet. For instance, if a server
        is temporarily unreachable, the request is requested in a fixed delay after the first failure.

        Example::

        > @Decorators.retry_with_exponential_stalling(5)
        > 1 def foo(x):
        >    ...
        > 7 foo(10)
        > # console prints: Trying to execute $foo
        > # upon failure: stalls a multiple of 2 seconds and tries a next execution after stalling.
        > # after 5 tries, it raises an error

        :param times: how many tries to execute the function
        :type times: int
        :param white_noise: if set to True it adds some random values to the stalling period
        :type white_noise: bool
        :return: a decorated function which tries to execute a specified times and sleeps during two failures. The sleeping time increases exponentially
        :rtype: func
        """

        def decorator(func):
            """
            Wraps decorator arguments
            """

            @wraps(func)
            def wrapper(*args, **kwargs):
                """
                Wraps the original function and adds the decorator's retry with exponential stalling functionality
                """
                t, delay = 1, 2 if not white_noise else 2 + random()
                while t <= times:
                    try:
                        log.info(f'Trying to execute "{func.__name__}" ({t}/{times})')
                        res = func(*args, **kwargs)
                        log.info(f'Successfully executed "{func.__name__}".')
                        return res
                    except Exception as e:
                        log.warning("Execution failed for the following reason:", e)
                        t += 1
                        if t <= times:
                            log.info(
                                f"Stalling {round(delay, 3)} secs before next execution try."
                            )
                            time.sleep(delay)
                            delay *= 2
                        else:
                            log.error(
                                f'Function "{func.__name__}" could not be executed after {times} tries'
                            )
                            raise FunctionNotExecutedError(f'Function "{func.__name__}" could not be executed after {times} tries for the following reason: {e}')

            return wrapper

        return decorator

    @staticmethod
    def accepted_arguments(accepted_args:list):
        '''
        When decorating a function with this decorator, the function's arguments are checked against a list of valid arguments.
        If an invalid argument is encoutered, the function is not executed.

        Example::

        > @Decorators.accepted_arguments([0,1])
        > 1 def foo(x):
        >    ...
        > 7 foo(10)
        > # console prints: Encountered a non-valid argument.
        > # console prints: Valid arguments are: [0,1]

        :param accepted_args: list of accepted arguments by the function
        :type accepted_args: list
        :return: a decorated function which checks the aguments
        '''
        def decorator(func):
            @wraps(func)
            def wrapper(*args):
                try:
                    assert all([a in accepted_args for a in args])
                except AssertionError:
                    raise SyntaxError(f'Encountered a non-valid argument.\nValid arguments are: {accepted_args}')
                result = func(*args)
                return result
            return wrapper
        return decorator

    @staticmethod
    def accepted_arguments_within_class_methods(accepted_args):
        '''
        When decorating a function with this decorator, the function's arguments are checked against a list of valid arguments.
        If an invalid argument is encountered, the function is not executed. This decorator is basically the same as "accepted_arguments"
        decorator except that it is aimed for functions within classes (i.e. containing a "self" parameter). In these setup, the class instance
        itself is passed as the first argument. Therefore, this Decorator only checks the second till last argument for correctness.

        Example::

        > 1 class Foo:
        > 2   ...
        > ...
        > 10   @Decorators.accepted_arguments_within_class_methods([0,1])
        > 11   def bar(self):
        > 12         ...
        > ...
        > 18 foo=Foo(1)
        > 19 foo.bar()
        > # console prints: Encountered a non-valid argument.
        > # console prints: Valid arguments are: [0,1]

        :param accepted_args: list of accepted arguments by the function
        :type accepted_args: list
        :return: a decorated function which checks the aguments
        '''
        def decorator(func):
            @wraps(func)
            def wrapper(*args):
                try:
                    assert all([a in accepted_args for a in args[1:]])
                except AssertionError:
                    raise SyntaxError(f'Encountered a non-valid argument.\nValid arguments are: {accepted_args}')
                result = func(*args)
                return result
            return wrapper
        return decorator

    @staticmethod
    def accepted_argument_types(*decorator_args):
        '''
        When decorating a function with this decorator, the function's arguments types are checked against a list of valid types.
        The types are provided in the same order as the corresponding arguments such that they match.

        Example::

        > @Decorators.accepted_argument_types(str,str)
        > 1 def foo(x,y):
        >    ...
        > 7 foo(10,5)
        > # console prints: Argument Types do not match expected types.
        > # console prints: Expected str, str but got int, int

        :param decorator_args:
        :return:
        '''
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                check_args = dict(zip(decorator_args, args))
                for argument_types, arguments in check_args.items():
                    try:
                        assert isinstance(arguments, argument_types)
                    except AssertionError:
                        raise TypeError(f'Argument Types do not match expected types.\nExpected {type(arguments)} but got {argument_types}')
                result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator

    @staticmethod
    def class_object_has_attr(attribute):
        '''
        When decorating a class method with this function, it checks if the class instance has a given attribute.
        It allows chaining to get deep levels of attributes. Note that this decorator can only be used by class methods.

        :param attribute:
        :return:
        '''
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    assert has_deep_attr(args[0], attribute)
                    result = func(*args, **kwargs)
                    return result
                except AssertionError:
                    log.error(f"The object '{object}' does not have the required attribute {attribute}.")
            return wrapper
        return decorator

    @classmethod
    def container_non_empty(cls, func):
        '''
        When decorating a function with this decorator, the function checks if the object is not empy.

        Example::

        > @Decorators.container_non_empty
        > 1 def foo(x):
        >    ...
        > 7 foo('')
        > # console prints: Container '' is empty

        :param decorator_args:
        :return:
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            for argument in args:
                if cls._is_container(argument):
                    cls._check_if_empty_container(argument)
            result = func(*args, **kwargs)
            return result

        return wrapper

    @staticmethod
    def _is_container(obj):
        """
        Indicates, if an object is a container by checking if is has the __iter__ attribute

        :param obj: an object whose type is tested
        :return: True if it is a container object
        :rtype: bool
        """
        return hasattr(type(obj), '__iter__')

    @staticmethod
    def _check_if_empty_container(obj) -> None:
        """
        Checks if the function's argument is a container object.
        It currently only works for list, dict, str, tuple and set object. Further object types can be added by time.

        :param obj: an object, whose size is tested
        :return: None
        :raises IndexError if the container is empty

        """
        obj_type = type(obj)
        cond = {
            list: len,
            dict: len,
            str: len,
            tuple: len,
            set: len,
            # np.ndarray : np.size,
            # pd.core.frame.DataFrame : len, #or pd.core.frame.DataFrame.empty
        }
        func = cond[obj_type]
        if not func(obj):
            raise IndexError(f'Container {obj} is empty')


class Dict_to_Obj:
    '''
    This class constructs an object notation out of a dictionary.
    '''
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)


class ClassAttrHandler(object):
    '''
    This class provides some functionalities with respect to class instance attributes.
    Additional functionalities allow iterating over the object, transform all container attributes to their corresponding
    size, deleting empty attributes and getting a list of strings containg all attributes label or attribute values.
    Usage: costume classes can inherit from this class in order to have additional functionalities with respect to attributes.

    Example::


    > 1 class Myclass(ClassattrHandler):
    > 2   def __init__(self,attribute_1, attribute_2):
    > 3       self.attribute_1 = attribute_1
    > 4       self.attribute_2 = attribute_2
    > 5       ...
    > 6
    > 7   def foo(self):
    > 8       for attr_label, attr_value in self:
    > 9           ....
    > 10  def print_attr_labels(self):
    > 11      print(self.attributes_labels)
    '''

    def __iter__(self):
        '''
        Enables class attributes to be iterated over. Simply let the target class this class.
        Class attributes can then be iterated over by using a for loop.

        Example:
            def Myclass(ClassattrHandler):
                def __init__(....

                def iterage_over_attibutes(self):
                    for attr, value in self:
                        ...

        In this Example, the class "Myclass" inherits the ClassAttrHandler which therefore allows it to iterate over its attributes.
        This is achieved via a "for ... in self" loop which yields the attributes and the corresponding value
        '''
        for attr, value in self.__dict__.items():
            yield attr, value

    def _return_container_size(self):
        '''
        Transforms all class instances attributes of container type into its corresponding length.

        :return: all attributes represent their length value
        '''
        for i in self:
            if Decorators._is_container(i[0]):
                self.__dict__[i[0]] = len(i[1])
            else:
                self.__dict__[i[0]] = 'No Container attribute'

    def _delete_empty_attributes(self):
        '''
        Drop all attributes which are empty from the instance.

        :return: the same object which no longer has any empty attribute
        '''
        attrs_to_delete = [val for val,attr in self if not attr]
        for attr in attrs_to_delete:
            delattr(self,attr)

    @property
    def attributes_labels(self, attr_type=None):
        '''
        Returns a list of an object's attributes labels. If provided with attr_type, only attributes labels of a certain type are written into the list

        :param attr_type: Optional argument to restrict the attribute list to attributes of the given type.
        :return: a list of strings containing all attributes labels
        '''
        return [attr_label for attr_label, attr_val in self] if not attr_type else [attr_label for attr_label, attr_val
                                                                                    in self if
                                                                                    isinstance(attr_val, attr_type)]
    @property
    def attributes_values(self, attr_type=None):
        '''
        Returns a list of an object's attributes values. If provided with attr_type, only attributes values of a certain type are written into the list

        :param attr_type: Optional argument to restrict the attribute list to attributes of the given type.
        :return: a list of strings containing all attributes values
        '''
        return [attr_val for attr_label, attr_val in self] if not attr_type else [attr_val for attr_label, attr_val in
                                                                                  self if
                                                                                  isinstance(attr_val, attr_type)]
    @staticmethod
    def get_deep_attr(obj, attrs):
        '''
        This function is a helper function which allows attributes checking for nested/composed attributes.

        :param obj:
        :param attrs:
        :return:
        '''
        for attr in attrs.split("."):
            obj = getattr(obj, attr)
        return obj

    @staticmethod
    def has_deep_attr(obj, attrs):
        '''
        This function is a helper function which allows attributes checking for nested/composed attributes.

        :param obj:
        :param attrs:
        :return:
        '''
        try:
            get_deep_attr(obj, attrs)
            return True
        except AttributeError:
            return False
