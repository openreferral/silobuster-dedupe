"""
SingletonMeta turns a class into a Singleton class. There are numerous methods on StackOverflow to accomplish this. As of Python 3.6, all methods have nuances and have unexpected behavior except for this method.

USAGE:

class MyClass(metaclass=SingletonMeta):
    pass

NOTES: MetaClass is a class that inherits type. Type is called when an object is created. class MyObject is equivalent to
type(MyObject, bases, args) ..

Here a metaclass returns the instance that has already been created. This method is preferred over the "new"
dunder method returning the instance. In that method, properties do not behave correctly.

"""

class SingletonMeta(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        
        return cls._instance
