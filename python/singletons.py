"""
    Singleton classes
"""
import functools
import threading

class Singleton(type):
    """
    Singleton Metaclass
    
    Python Singleton Metaclass that creates a Singleton Data Pattern for Python Classes
    <http://en.wikipedia.org/wiki/Singleton_pattern>
    
    Usage of this class also handles inheritance. If a class inherits from a class that uses this
    metaclass, this pattern will consider the inherited class to also be an instance.
    
    """
    _SingletonLock = threading.RLock()
    _SingletonInstance = None
    
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._SingletonInstance = None
        
    def __call__(cls,*args,**kw):
        if cls._SingletonInstance is None:
            with cls._SingletonLock:
                if cls._SingletonInstance is None:
                    cls._SingletonInstance = super(Singleton, cls).__call__(*args, **kw)
        return cls._SingletonInstance
    
    def __new__(cls, nameStrIn, basesTupleIn, localsDictIn):
        with cls._SingletonLock:
            # Handle Singleton Inheritance
            
            # Check for the singleton metaclass
            for currentBaseObj in basesTupleIn:
                if hasattr(currentBaseObj, "__metaclass__"):
                    # Check for _SingletonInstance
                    if hasattr(currentBaseObj, "_SingletonInstance"):
                        # Get the singleton instance
                        instanceObj = currentBaseObj()
                        
                        # Copy over the instance attributes
                        for keyStr, valueVoid in instanceObj.__dict__.items():
                            if keyStr not in localsDictIn:
                                localsDictIn[keyStr] = valueVoid                    
                    
        # Return the new instance
        return super(Singleton, cls).__new__(cls, nameStrIn, basesTupleIn, localsDictIn)
