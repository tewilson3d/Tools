"""
Override shutil methods to allow file copy progress
"""
######################################
############# IMPORTS ################
######################################
import os
import stat
import shutil

######################################
############# DEFINES ################
######################################
#: Base Copy Length
BASE_COPY_LENGTH = 16 * 1024 # 16kb

######################################
############# FUNCTIONS ##############
######################################
def copyfileobj(fsrcObjIn, 
                fdstObjIn, 
                lengthIntIn=BASE_COPY_LENGTH,
                callbackFuncIn=None):
    """
    shutil copyfileobj override with progress callback
    
    Args:
        fsrcObjIn (obj): Source File Object
        fdstObjIn (obj): Destination File Object
        
    Keyword Args:
        lengthIntIn (int): Read Length
        callbackFuncIn (func): Progress Callback
        
        
    return:
        None
    """
    writtenLengthInt = 0
    srcSizeInt = os.path.getsize(fsrcObjIn.name)
    
    while 1:
        buf = fsrcObjIn.read(lengthIntIn)
        if not buf:
            break
        
        fdstObjIn.write(buf)
        
        # Callback
        writtenLengthInt += lengthIntIn
        
        try:
            if callbackFuncIn is not None:
                callbackFuncIn(writtenLengthInt, 
                               srcSizeInt)
        except Exception as errorObj:
            pass
 
def copyfile(srcFileStrIn, 
             dstFileStrIn,
             lengthIntIn=BASE_COPY_LENGTH,
             callbackFuncIn=None):
    """
    shutil copyfile override with progress callback
    
    Args:
        srcFileStrIn (str): Source File
        dstFileStrIn (str): Destination File
        
    Keyword Args:
        lengthIntIn (int): Copy Length
        callbackFuncIn (func): Progress Callback
        
    Returns:
        None
    """
    if shutil._samefile(srcFileStrIn, dstFileStrIn):
        raise shutil.Error("`{0}` and `{1}` are the same file".format(srcFileStrIn, dstFileStrIn))

    for fn in [srcFileStrIn, dstFileStrIn]:
        try:
            st = os.stat(fn)
        except OSError:
            # File most likely does not exist
            pass
        else:
            # XXX What about other special files? (sockets, devices...)
            if stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError("`{0}` is a named pipe".format(fn))

    with open(srcFileStrIn, 'rb') as fsrc:
        with open(dstFileStrIn, 'wb') as fdst:
            copyfileobj(fsrc, 
                        fdst,
                        lengthIntIn=lengthIntIn,
                        callbackFuncIn=callbackFuncIn)
            
            
def copy(srcFileStrIn, 
         dstFileStrIn,
         lengthIntIn=BASE_COPY_LENGTH,
         callbackFuncIn=None):
    """
    shutil copy override with progress callback
    
    Args:
        srcFileStrIn (str): Source File
        dstFileStrIn (str): Destination File
        
    Keyword Args:
        lengthIntIn (int): Copy Length
        callbackFuncIn (func): Progress Callback
        
    Returns:
        None
    """
    if os.path.isdir(dstFileStrIn):
        dstFileStrIn = os.path.join(dstFileStrIn, os.path.basename(srcFileStrIn))
    copyfile(srcFileStrIn, 
             dstFileStrIn,
             lengthIntIn=lengthIntIn,
             callbackFuncIn=callbackFuncIn)
    shutil.copymode(srcFileStrIn, dstFileStrIn)    
    
    
######################################
############# CLASSES ################
######################################

######################################
############### MAIN #################
######################################
if __name__ == "__main__":
    pass