# Utilities_Import
This module contains [Python](https://www.python.org/) objects which are intended to faciliate other Python code and help to inspect it. It can be imported and used in other modules. 
Currently, the following four classes are found in this module:
 - *Logger:* this class initializes a logging instance which can be used to log all activities.
 - *Decorators:* this class provides a set of different Decorators which can be used to add functionalities to functions. The following decorating functions are found
    - *run_time:* Indicates the function's run time in a hh:mm:ss
    - *show_args:* Indicates the arguments passed to the function
    - *counter:* Indicates how often the function has been called
    - *retry :* Tries to execute the function. Upon failure, retries execution after a stalling time. If it hits the limit of tries or executes successfully, control is passed to the following line
    - *retry_with_exponential_stalling:* Similar to *retry*. Does not take a fixed stalling time but an exponential increasingly
    - *accepted_arguments:* Checks the accepted arguments for the function and raises an Exception if those are not met
    - *accepted_arguments_within_class_methods:* Similar as *accepted_arguments*. Intended for class methods however
    - *accepted_argument_types:* Checks the accepted argument types for the function and raises an Exception if those are not met
    - *class_object_has_attr:* checks if a class has a given attribute
    - *container_non_empty:* checks if a container object (tuple,set,dict,list,str) is not empty
 - *ClassAttrHandler:* this class provides some functionalities with respect to classes and their respective attributes.
 - *Dict_to_Obj:* converts a dictionary to an object notation

The src file can be imported and used for other projects. 

# Prerequisits
The source code is written in [Python 3.8](https://www.python.org/). It use some of the standard libraries which are included in the most Python environments.
Those standard libraries are:

    - os
    - logging
    - sys
    - random
    - time
    - functools

# Installation
You can clone this repository by running:
	
	git clone https://github.com/dheinz0989/Utilities_Import

# Example usage
an example usage can be found in the [test](https://github.com/dheinz0989/Utilities_Import/tree/master/test). It imports most of the modules features and includes them in a test script. 
You can run it via:

```
python example.py
```
# Documentation
More details with regards to the function and for which use case they are intended to be used can be found in the [docs](https://github.com/dheinz0989/Utilities_Import/blob/master/docs/build/html/Utilities_Import.html). 

# To Do
This repository has several things which are not implemented yet. Amongs others, the following implementation are planned:
1. Logger: add option for color
2. Logger: add options for not autmatically writing log files
3. ClassAttrHandler: bug in filtering class attributes
4. Decorators: add function for argument type checks for class methods