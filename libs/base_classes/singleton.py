"""
SingletonMeta turns a class into a Singleton class. There are numerous methods on StackOverflow to accomplish this. As of Python 3.6, all methods have nuances and have unexpected behavior except for this method.

USAGE:

class MyClass(metaclass=SingletonMeta):
    pass

NOTES: MetaClass is a class that inherits type. Type is called when an object is created. class MyObject is equivalent to
type(MyObject, bases, args) ..

Here a metaclass returns the instance that has already been created. This method is preferred over the "new"
dunder method returning the instance. In that method, properties do not behave correctly.

The __init__ method creates an _instance attribute and sets it equal to None. The __call__ method checks if the _instance attribute exists. If it does, it returns that instance. If the _instance
attribute does not exist, it instantiates the class using the super() method and sets that instance equal to the _instance class attribute.
"""

class SingletonMeta(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        
        return cls._instance
