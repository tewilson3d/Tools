######################################
############# IMPORTS ################
######################################
import re
import inspect
import types

######################################
############# DEFINES ################
######################################
WRAP_SEMI_PRIVATES = False


############## preliminary: two utility functions #####################

def skip_redundant(iterable, skipset=None):
    """Redundant items are repeated items or items in the original skipset."""
    if skipset is None: skipset = set()
    for item in iterable:
        if item not in skipset:
            skipset.add(item)
            yield item


def remove_redundant(metaclasses):
    skipset = set([types.ClassType])
    for meta in metaclasses: # determines the metaclasses to be skipped
        skipset.update(inspect.getmro(meta)[1:])
    return tuple(skip_redundant(metaclasses, skipset))

##################################################################
## now the core of the module: two mutually recursive functions ##
##################################################################

memoized_metaclasses_map = {}

def get_noconflict_metaclass(bases, left_metas, right_metas):
    """Not intended to be used outside of this module, unless you know
    what you are doing."""
    # make tuple of needed metaclasses in specified priority order
    metas = left_metas + tuple(map(type, bases)) + right_metas
    needed_metas = remove_redundant(metas)

    # return existing confict-solving meta, if any
    if needed_metas in memoized_metaclasses_map:
        return memoized_metaclasses_map[needed_metas]
    # nope: compute, memoize and return needed conflict-solving meta
    elif not needed_metas:         # wee, a trivial case, happy us
        meta = type
    elif len(needed_metas) == 1: # another trivial case
        meta = needed_metas[0]
    # check for recursion, can happen i.e. for Zope ExtensionClasses
    elif needed_metas == bases: 
        raise TypeError("Incompatible root metatypes", needed_metas)
    else: # gotta work ...
        metaname = '_' + ''.join([m.__name__ for m in needed_metas])
        meta = classmaker()(metaname, needed_metas, {})
    memoized_metaclasses_map[needed_metas] = meta
    return meta

def classmaker(left_metas=(), right_metas=()):
    def make_class(name, bases, adict):
        metaclass = get_noconflict_metaclass(bases, left_metas, right_metas)
        return metaclass(name, bases, adict)
    return make_class



######################################
############# CLASSES ################
######################################
class BaseMetaClass(type):
    """
    Meta Class for Base Objects
    """
    def __init__(classObjIn,
                 nameStrIn,
                 basesListIn,
                 localsDictIn):
        # Set the class name
        classObjIn.__metricName__ = nameStrIn
        
        # Init the class
        super(BaseMetaClass, classObjIn).__init__(nameStrIn,
                                                  basesListIn,
                                                  localsDictIn)

    def __new__(classObjIn,
                nameStrIn,
                basesListIn,
                localsDictIn):
        for attrStr in localsDictIn:
            # Get the local value
            valueVoid = localsDictIn[attrStr]
            
            # Is this a function?
            if isinstance(valueVoid, types.FunctionType):
                # Ignore internals
                if re.match("__[a-zA-Z]*__", attrStr):
                    continue
                
                # Ignore Semi Privates
                if attrStr.startswith("_"):
                    if not WRAP_SEMI_PRIVATES:
                        continue

        # Return the class
        return super(BaseMetaClass, classObjIn).__new__(classObjIn,
                                                        nameStrIn,
                                                        basesListIn,
                                                        localsDictIn)
