######################################
############# IMPORTS ################
######################################
import fnmatch
import functools

import os
import re
import stat
import shutil
#import glob
import contextlib

import shutilOverride
#import metaclasses

######################################
############# DEFINES ################
######################################
#: Windows FilePath Types
FILEPATH_TYPE_UNDEFINED = -1
FILEPATH_TYPE_WINDOWS = 0
FILEPATH_TYPE_UNIX = 1
FILEPATH_TYPE_DEPOT = 2
FILEPATH_TYPE_MAYA = 3

#: FilePath Seperators
FILEPATH_SEPERATOR_WINDOWS = "\\"
FILEPATH_SEPERATOR_UNIX = "/"
FILEPATH_SEPERATOR_DEPOT = FILEPATH_SEPERATOR_UNIX
FILEPATH_SEPERATOR_MAYA = FILEPATH_SEPERATOR_UNIX


######################################
############# CLASSES ################
######################################
class FilePath(str):
    """
    FilePath Class

    Because :py:class:`FilePath` inherits from a built-in immutable type, we cannot modify the string in the __init__ call
    because the object is already constructed.  Moving the functionality to __new__ allows us to construct
    a new string that has been modified by os.path.normpath.

    See <http://stackoverflow.com/questions/2673651/inheritance-from-str-or-int> for more information

    Attributes:
        pathStr (str): FilePath

    Args:
        pathStrIn (str): FilePath
    """
    ## Set the metaclass
    #__metaclass__ = metaclasses.classmaker(left_metas=(metaclasses.BaseMetaClass,),
                                           #right_metas=())

    def __init__(self,
                 valueVoidIn,
                 pathTypeIntIn=FILEPATH_TYPE_UNDEFINED):
        """
        FilePath Init

        Args:
            clsObjIn (obj): Class Object
            valueVoidIn (void): Value to init

        Keyword Args:
            pathTypeIntIn (int): FilePath Type (For Seperators)
        """
        # Set the path type
        self.pathTypeInt = pathTypeIntIn

    def __new__(clsObjIn,
                valueVoidIn,
                pathTypeIntIn=FILEPATH_TYPE_UNDEFINED):
        """
        ___new___ Override

        Args:
            clsObjIn (obj): Class Object
            valueVoidIn (void): Value to init

        Keyword Args:
            pathTypeIntIn (int): FilePath Type (For Seperators)

        Returns:
            (object): Constructed :py:class:`FilePath` Object
        """
        # Ensure we have a proper type
        if not isinstance(valueVoidIn, (str, type(clsObjIn))):
            raise Exception("Invalid type for path initialization: {0}".format(type(valueVoidIn)))

        # Build the path
        pathStr = str(valueVoidIn)
        pathTypeInt = -1

        # See if we are getting a path object
        if isinstance(valueVoidIn, FilePath):
            # The `pathTypeIntIn` is the authoratative value
            if pathTypeIntIn != FILEPATH_TYPE_UNDEFINED:
                pathTypeInt = pathTypeIntIn
            else:
                # Set to the FilePath's Type if not `FILEPATH_TYPE_UNDEFINED`
                if valueVoidIn != FILEPATH_TYPE_UNDEFINED:
                    pathTypeInt = valueVoidIn.pathTypeInt
                else:
                    # Default to windows
                    pathTypeInt = FILEPATH_TYPE_WINDOWS
        else:
            if pathTypeIntIn != FILEPATH_TYPE_UNDEFINED:
                pathTypeInt = pathTypeIntIn
            else:
                # Default to windows
                pathTypeInt = FILEPATH_TYPE_WINDOWS

        # Convert the seperators
        if pathTypeInt == FILEPATH_TYPE_WINDOWS:
            pathStr = os.path.normpath(pathStr)
            pathStr = pathStr.replace(os.path.sep, FILEPATH_SEPERATOR_WINDOWS)
        elif pathTypeInt == FILEPATH_TYPE_UNIX:
            pathStr = os.path.normpath(pathStr)
            pathStr = pathStr.replace(os.path.sep, FILEPATH_SEPERATOR_UNIX)
        elif pathTypeInt == FILEPATH_TYPE_DEPOT:
            pathStr = pathStr.replace(os.path.sep, FILEPATH_SEPERATOR_DEPOT)
        elif pathTypeInt == FILEPATH_TYPE_MAYA:
            pathStr = os.path.normpath(pathStr)
            pathStr = pathStr.replace(os.path.sep, FILEPATH_SEPERATOR_UNIX)

        newObj = super(FilePath, clsObjIn).__new__(clsObjIn,
                                                   pathStr)
        newObj.pathTypeInt = pathTypeInt

        return newObj

    def __eq__(self,
               otherStrIn):
        """
        __eq__ (==) override

        Args:
            otherStrIn (str): Comparison String

        Returns:
            (bool)
        """
        if otherStrIn is None:
            return False

        # Return a relative path comparison
        convertedPathObj = None

        try:
            convertedPathObj = self.relativePath(FilePath(otherStrIn))
        except Exception as errorObj:
            convertedPathObj = None

        if convertedPathObj is not None:
            return str(convertedPathObj) == "."
        else:
            return str(self) == convertedPathObj

    def __ne__(self,
               otherStrIn):
        """
        __ne__ (!=) override

        Args:
            otherStrIn (str): Comparison String

        Returns:
            (bool)
        """
        if otherStrIn is None:
            return False

        # Return a relative path comparision
        convertedPathObj = None

        try:
            convertedPathObj = self.relativePath(FilePath(otherStrIn))
        except Exception as errorObj:
            convertedPathObj = None

        if convertedPathObj is not None:
            return str(convertedPathObj) != "."
        else:
            return str(self) != convertedPathObj

    def __repr__(self):
        """
        __repr__ override
        """
        return "FilePath('{0}')".format(self)

    @classmethod
    def _convertToPath(self,
                       pathVoidIn):
        """
        Ensure that `pathVoidIn` is a `filepath\.FilePath` instance

        Args:
            pathVoidIn (void): (str/FilePath) FilePath

        Returns:
            (object): `filepath\.FilePath` Instance

        Raises:
            (:class:`Exception`): Invalid Type
        """
        if isinstance(pathVoidIn, (str)):
            return FilePath(pathVoidIn)
        elif isinstance(pathVoidIn, type(self)):
            return pathVoidIn
        else:
            raise Exception("Invalid Object Type: {0}".format(type(pathVoidIn)))

    def absolutePath(self):
        """
        Returns the absolute path

        Args:
            None

        Returns:
            (object) :class:`filepath\.FilePath`
        """
        return FilePath(os.path.abspath(self))

    def relativePath(self,
                     sourcePathVoidIn):
        """
        Returns the paths relative

        Return the relative path to `sourcePathVoid`

        Args:
            sourcePathVoid (void): (str/:class:`FilePath`) Source FilePath

        Returns:
            (object): :class:`filepath\.FilePath` Relative FilePath
        """
        # Convert to a FilePath instance if `sourcePathVoid` is a string
        sourcePathObj = None

        try:
            sourcePathObj = FilePath._convertToPath(sourcePathVoidIn)
        except Exception as errorObj:
            return self

        # Return the relative path
        try:
            return FilePath(os.path.relpath(self, sourcePathObj.absolutePath()))
        except ValueError as errorObj:
            return self

        return sourcePathObj

    def caseSensitivePath(self):
        """
        Returns the case sensitive path

        Returns the case sensitive path, same case as actual local directories.
        If the path does not exist, the path casing is converted as much as possible.

        Args:
            None

        Returns:
            (object) :class:`filepath\.FilePath` Case Sensitive FilePath
        """

        if self.startswith(os.path.sep):
            return self

        # Split the string
        dirsList = self.stringSplit(os.path.sep)

        # Start with the disk letter, I.E. "C:"
        caseSensitivePathList = [dirsList.pop(0).upper()]

        while len(dirsList) > 0:

            # Search subfolders/files for the next part of our path
            targetName = dirsList[0].lower()
            foundNext = False

            for objectOnDisk in os.listdir(os.path.sep.join(caseSensitivePathList) + os.path.sep):
                if targetName == objectOnDisk.lower():
                    caseSensitivePathList.append(objectOnDisk)
                    dirsList.pop(0)
                    foundNext = True
                    break

            # If we didn't find the path, it means we have to trust our input from here on out
            if not foundNext:
                caseSensitivePathList.extend(dirsList)
                dirsList = []

        return FilePath(os.path.sep.join(caseSensitivePathList))

    def join(self,
             pathsVoidIn):
        """
        Joins the list of paths to this path

        Args:
            pathsVoidIn (void): Expected List of strings or string

        Returns:
            (object): :class:`filepath\.FilePath` Joined FilePath
        """
        # Joined Paths
        joinPathsList = [str(self)]

        if isinstance(pathsVoidIn, list):
            joinPathsList.extend(pathsVoidIn)
        else:
            joinPathsList.append(pathsVoidIn)

        # Return the joined path
        return FilePath(functools.reduce(lambda sPathA, sPathB: os.path.join(str(sPathA), str(sPathB)),
                                         joinPathsList),
                        self.pathTypeInt)

    def stringJoin(self,
                   iterableVoidIn):
        """
        String Join

        Args:
            iterableVoidIn (void): Iterable Object

        Returns:
            (str): Joined String
        """
        return FilePath(str.join(self, iterableVoidIn),
                        self.pathTypeInt)

    def baseName(self):
        """
        Returns the base name of the path

        Args:
            None

        Returns:
            (object): :class:`filepath\.FilePath` Base Name
        """
        return FilePath(os.path.basename(self))

    def isChildOf(self,
                  otherPathStrIn):
        """
        Returns whether this path is a child of the given path

        Args:
            otherPathStrIn (str): The path to be tested against

        Returns:
            (bool): Is `otherPathStrIn` as child of the path
        """
        sRelativePath = ""

        try:
            sRelativePath = os.path.relpath(self, otherPathStrIn)
        except ValueError as pError:
            # ValueError is thrown when the paths are in different drives
            return False

        return not sRelativePath.startswith(os.pardir + os.path.sep)

    def containVars(self):
        """
        Determine if the string contains vars

        Determine if the string contains either $ or % characters

        Args:
            None

        Returns:
            (bool): Contains Vars
        """
        if "$" in self or "%" in self:
            return True

        return False

    def copy(self,
             destinationVoidIn,
             lengthIntIn=shutilOverride.BASE_COPY_LENGTH,
             progressCallbackFuncIn=None):
        """
        Copies the path to the destination path

        Args:
            destinationVoidIn (str/object): Destination FilePath

        Keyword Args:
            lengthIntIn (int): Copy Length
            progressCallbackFuncIn (func): Progress Callback Func - Function needs to be formatted with the following arguments <Current Written Size>, <Total File Size>

        Returns:
            (object): :class:`filepath\.FilePath` Destination Directory

        Raises:
            (`Exception`): If destination cannot be written
        """
        # Convert the path
        destinationPathObj = FilePath._convertToPath(destinationVoidIn)

        try:
            if self.isDir():
                # Copy the dir
                shutil.copytree(self, destinationPathObj)
            else:
                if destinationPathObj.isDir():
                    # Join the destination path
                    destinationPathObj = destinationPathObj.join(self.basename())

                # If the folder doesn't exist, make it
                if not destinationPathObj.dir().exists():
                    destinationPathObj.dir().makeDir()

                shutilOverride.copy(self, 
                                    destinationPathObj,
                                    lengthIntIn=lengthIntIn,
                                    callbackFuncIn=progressCallbackFuncIn)
        except Exception as pError:
            raise Exception("copy(): {0} -- {1}".format(destinationPathObj, pError))

        return destinationPathObj

    def dir(self):
        """
        Returns the directory name of the path

        Args:
            None

        Returns:
            (object): :class:`filepath\.FilePath` Directory Name
        """
        #for d in range(2):
            #if d == 0:    
                #np = os.path.dirname(a)
            #else:
                #np = os.path.dirname(np)
        
        return FilePath(os.path.dirname(self.absolutePath()))

    def exists(self):
        """
        Return if the path exists

        Args:
            None

        Returns:
            (bool): FilePath Exists
        """
        if (self != '.'):
            return os.path.exists(self)
        else:
            return False

    def convertToPythonImport(self,
                              pythonPathStrIn=None):
        """
        Convert a path to a Python Import FilePath (%PYTHONPATH%\core\general\path.py to core.general.path)

        Args:
            pythonPathStrIn (str): Python FilePath

        Returns:
            (str): Converted Python Import FilePath
        """
        # Make sure `pythonPathStrIn` ends with a "\"
        if pythonPathStrIn is None:
            pythonPathStr = self
        else:
            pythonPathStr = pythonPathStrIn

        if not pythonPathStr.endswith(os.path.sep):
            pythonPathStr = "{0}{1}".format(pythonPathStr, os.path.sep)

        # Remove the python path
        removedPythonPathStr = self.caseInsensitiveReplace(pythonPathStr, "")

        # Remove the extension
        pathStr, extStr = os.path.splitext(removedPythonPathStr)

        # Replace the seperator with "."
        pythonImportPathStr = pathStr.replace(os.path.sep, ".")

        return pythonImportPathStr

    def caseInsensitiveReplace(self,
                               findStrIn,
                               replaceStrIn,
                               countIntIn=0):
        """
        Do a case insensitive replace of `findStrIn` with `replaceStrIn`

        Args:
            findStrIn (str): String to Find
            replaceStrIn (str): String to Replace

        Keyword Args:
            countIntIn (int): Times to replace. -1 is infinite

        Returns:
            (str): String with `findStrIn` replaced with `replaceStrIn`
        """
        # Do a RE sub
        reObj = re.compile(re.escape(findStrIn), re.IGNORECASE)
        subStr = reObj.sub(replaceStrIn, self, count=countIntIn)

        return subStr

    def expandvars(self):
        """
        Returns os.path.expandvars(self)

        Args:
            None

        Returns:
            (object): :class:`filepath\.FilePath` Expanded Vars FilePath
        """
        return FilePath(os.path.expandvars(self))

    def getExt(self):
        """
        Returns the extension of the path

        Args:
            None

        Returns:
            (str): Extension
        """
        return os.path.splitext(self)[1]

    def getFileName(self):
        """
        Returns the name of the path without file extension

        Args:
            None

        Returns:
            (str): File Name
        """
        return os.path.splitext(self)[0]

    def getBaseFileName(self):
        """
        Returns the name of the basename without file extension

        Args:
            None

        Returns:
            (str): File Name

        Examples::

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from path import FilePath
                >>> FilePath("C:/Windows/notepad.exe").getBaseFileName()

        """
        return os.path.splitext(os.path.basename(self))[0]
    
    def getModifiedTime(self):
        """
        Returns the last modified time of the path

        Args:
            None

        Returns:
            (float): Modified Time
        """
        return os.path.getmtime(self)

    def getSize(self):
        """
        Returns the size of the path

        Args:
            None

        Returns:
            (int): File Size
        """
        return os.path.getsize(self)

    def isBinary(self,
                 chunkSizeIntIn=1024):
        """
        Returns True if the path is a binary file. Otherwise it is text

        Args:
            None

        Keyword Args:
            chunkSizeIntIn (int): Chunk size to read from the file in order to determine the file type

        Returns:
            (bool): Is Binary
        """
        if not self.isFile():
            raise Exception("Not a file: {0}".format(self))

        isBinary = False

        with open(self, "rb") as handleObj:
            while True:
                chunkObj = handleObj.read(chunkSizeIntIn)

                # Null byte means binary
                if '\0' in chunkObj:
                    isBinary = True
                    break

                # Reached the end of the file
                if len(chunkObj) < chunkSizeIntIn:
                    break

        return isBinary

    def isDir(self):
        """
        Returns if the path is a directory

        Args:
            None

        Returns:
            (bool): FilePath is directory
        """
        return os.path.isdir(self)

    def isFile(self):
        """
        Returns if the path is a file

        Args:
            None

        Returns:
            (bool): FilePath is a file
        """
        return os.path.isfile(self)

    def isReadable(self):
        """
        Returns if the path is readable

        Args:
            None

        Returns:
            (bool): Is Readable
        """
        return os.access(self, os.R_OK)

    def isWritable(self):
        """
        Returns if the path is writable

        Args:
            None

        Returns:
            (bool): Is Writable
        """
        return os.access(self, os.W_OK)

    def makeDir(self):
        """
        Makes the directory path recursively

        Args:
            None

        Returns:
            (object): :class:`filepath\.FilePath`
        """
        if not self.exists():
            try:
                os.makedirs(self)
            except os.error as errorObj:
                raise Exception("Unable to make directory: {0} -- {1}".format(self, errorObj))

        return self

    def rename(self,
               newNameVoidIn):
        """
        Renames the path to the `newNameVoidIn`

        Args:
            newNameVoidIn (void): (str/:class:`filepath\.FilePath`) Destination Directory

        Returns:
            (object): :class:`filepath\.FilePath`

        Raises:
            (Exception): Directory Move Failed
        """
        try:
            os.rename(self, newNameVoidIn)
        except os.error as errorObj:
            raise Exception("File Rename Failed: {0} -- {1}".format(newNameVoidIn, errorObj))

    def move(self,
             destinationVoidIn):
        """
        Renames the path to the `destinationVoidIn`

        Args:
            destinationVoidIn (void): (str/:class:`filepath\.FilePath`) Destination Directory

        Returns:
            (object): :class:`filepath\.FilePath`

        Raises:
            (Exception): Directory Move Failed
        """
        destinationObj = FilePath._convertToPath(destinationVoidIn)

        try:
            os.renames(self, destinationObj)
        except os.error as errorObj:
            raise Exception("Directory Move Failed: {0} -- {1}".format(destinationObj, errorObj))

    @contextlib.contextmanager
    def openForRead(self):
        """
        Opens the path for read. Yields the opened file object

        Args:
            None

        Yields:
            (object): File Handle

        Raises:
            (Exception): Failed to open
            (Exception): FilePath is not a file
        """
        if not self.isFile():
            raise Exception("{0} is not a file".format(self))

        handleObj = None

        try:
            handleObj = open(self, "rU")
            yield handleObj
        except IOError as errorObj:
            raise Exception(errorObj)
        finally:
            if handleObj != None:
                handleObj.close()

    @contextlib.contextmanager
    def openForWrite(self):
        """
        Opens the path for write. Yields the opened file object

        Args:
            None

        Yields:
            (object): File Handle

        Raises:
            (Exception): Failed to open
            (Exception): FilePath is not a file
        """
        handleObj = None

        # See if the directory exists
        if not self.dir().exists():
            # Create the dir
            self.dir().makeDir()

        try:
            handleObj = open(self, "w")
            yield handleObj
        except IOError as errorObj:
            raise Exception(errorObj)
        finally:
            if handleObj != None:
                handleObj.close()

    def readLines(self):
        """
        Returns the list of text lines

        Args:
            None

        Returns:
            (list): Read Lines

        Raises:
            (Exception): Failed to open
            (Exception): FilePath is not a file
        """
        if not self.isFile():
            raise Exception("{0} is not a file".format(self))

        linesList = []

        with self.openForRead() as handleObj:
            linesList = handleObj.readlines()

        return linesList

    def readText(self):
        """
        Returns the text string of the file in the path

        Args:
            None

        Returns:
            (str): Read Lines

        Raises:
            (Exception): Failed to open
            (Exception): FilePath is not a file
        """
        if not self.isFile():
            raise Exception("{0} is not a file".format(self))

        outputStr = ""

        with self.openForRead() as handleObj:
            outputStr = handleObj.read()

        return outputStr

    def remove(self,
               isRecursiveIn=False,
               doForceIn=False):
        """
        Removes the path.

        If `isRecursiveIn` is True, remove all the directories leading to the file
        as well

        Args:
            isRecursiveIn (bool): If the remove should be done recursively
            doForceIn (bool): If we should make files writable to force the operation

        Returns:
            None
        """
        if doForceIn:
            if self.isDir():
                # Set all files writable
                pathsList = self.walk(isRecursiveIn=isRecursiveIn,
                                      isFileOnlyIn=False)

                for currentPathObj in pathsList:
                    currentPathObj.setWritable()
            else:
                self.setWritable()

        try:
            if self.isDir():
                if isRecursiveIn:
                    shutil.rmtree(str(self))
                else:
                    os.rmdir(self)
            else:
                try:
                    os.remove(self)
                except WindowsError as pError:
                    pass
        except Exception as pError:
            logging.warning(pError)

            raise Exception("Error removing path: {0}".format(self))

    def setReadOnly(self):
        """
        Sets the path to be read-only

        Args:
            None

        Returns:
            None
        """
        pathStatInt = os.stat(self)[0]

        if pathStatInt & stat.S_IWRITE:
            os.chmod(self, stat.S_IREAD)

    def setWritable(self):
        """
        Sets the path to be writable

        Args:
            None

        Returns:
            None
        """
        try:
            pathStatInt = os.stat(self)[0]

            if not (pathStatInt & stat.S_IWRITE):
                os.chmod(self, stat.S_IWRITE)
        except WindowsError as errorObj:
            logging.warning(errorObj)

    def walk(self,
             isRecursiveIn=False,
             maxDepthIntIn=-1,
             isFileOnlyIn=False,
             isDirOnlyIn=False,
             doMatchIn=False,
             matchModeStrIn="glob",
             matchStringsListIn=[],
             doIgnoreMatchIn=False,
             ignoreMatchModeStrIn="glob",
             ignoreMatchStringsListIn=[]):
        """
        Walks the directory path and returns a generator of all directires/files
        underneath.  User can match the path name with the given list of match
        strings accord to the `matchModeStrIn` ('glob' or 'regex').

        Args:
            None

        Keyword Args:
            isRecursiveIn (bool): If this should walk to the child directories
            maxDepthIntIn (int): Maximum depth to recurse to. -1 means infinite depth
            isFileOnlyIn (bool): If this should only include file paths
            isDirOnlyIn (bool): If this should only include directory paths
            doMatchIn (bool): If this should match the path name using `matchModeStrIn`
                             and `matchStringsListIn`
            matchModeStrIn (str): FilePath string matching mode: 'glob' or 'regex'
            matchStringsListIn (list): List of pattern strings for matching
            doIgnoreMatchIn (bool): If this should ignore paths that matches
                                   `ignoreMatchModeStrIn` and `ignoreMatchStringsListIn`
            ignoreMatchModeStrIn (str): FilePath string ignore matching mode: 'glob' or 'regex'
            ignoreMatchStringsListIn (list): List of pattern strings for ignore matching

        Yields:
            File Paths
        """
        def _matchPath(pathObjIn,
                       matchModeStrIn,
                       matchStringsListIn):
            """
            Helper function for walk().

            Returns True if the path matches at least one of the `i_lMatchStrings`,
            False otherwise

            Args:
                pathObjIn (object): :class:`filepath\.FilePath` Match FilePath
                matchModeStrIn (str): Match Mode: 'glob' or 'regex'
                matchStringsListIn (list): Match Strings

            Returns:
                (bool): Matched FilePath
            """
            absolutePathStr = pathObjIn.absolutePath()
            for matchStringStr in matchStringsListIn:
                if matchModeStrIn == "glob":
                    if fnmatch.fnmatch(absolutePathStr, matchStringStr):
                        return True
                elif matchModeStrIn == "regex":
                    matchObj = re.match(matchStringStr,
                                        absolutePathStr,
                                        flags=re.IGNORECASE)

                    if matchObj is not None:
                        return True

            return False

        def _appendPath(pathObjIn,
                        isMatchIn,
                        matchModeStrIn,
                        matchStringsListIn,
                        isIgnoreMatchIn,
                        ignoreMatchModeStrIn,
                        ignoreMatchStringsListIn):
            """
            Helper function for walk().  Appends the given path to `i_lPathList`
            if all match criteria are True

            Args:
                pathObjIn (object): :class:`filepath\.FilePath` FilePath
                isMatchIn (bool): Match FilePath
                matchModeStrIn (str): Matching Mode: 'glob' or 'regex'
                matchStringsListIn (list): Match Strings
                isIgnoreMatchIn (bool): Ignore Match
                ignoreMatchModeStrIn (str): Ignore Matching Mode: `glob` or `regex`
                ignoreMatchStringsListIn (list): Ignore Match Strings

            Returns:
                (bool): Append to path list
            """
            if not isMatchIn or (isMatchIn and _matchPath(pathObjIn, matchModeStrIn, matchStringsListIn)):
                if not isIgnoreMatchIn or (isIgnoreMatchIn and not _matchPath(pathObjIn, 
                                                                              ignoreMatchModeStrIn, 
                                                                              ignoreMatchStringsListIn)):
                    return True

            return False

        if isFileOnlyIn and isDirOnlyIn:
            raise ValueError("walk(): You cannot have file *AND* directories only!")

        # Initialize the output list
        levelInt = 0

        # Walk the path and grab only the ones that fit all criteria
        for dirPathStr, dirNamesList, filenamesList in os.walk(str(self)):
            # Create a FilePath instance
            dirPathObj = FilePath(dirPathStr)

            # Directory only
            if isDirOnlyIn or not (isDirOnlyIn or isFileOnlyIn):
                for dirNameStr in dirNamesList:
                    # Get the child directory
                    childDirtPathObj = dirPathObj.join(dirNameStr)

                    if _appendPath(childDirtPathObj,
                                   doMatchIn,
                                   matchModeStrIn,
                                   matchStringsListIn,
                                   doIgnoreMatchIn,
                                   ignoreMatchModeStrIn,
                                   ignoreMatchStringsListIn):
                        # Yield the child directory
                        yield childDirtPathObj

            # File Only
            if isFileOnlyIn or not (isDirOnlyIn or isFileOnlyIn):
                for filenameStr in filenamesList:
                    filePathObj = dirPathObj.join(filenameStr)

                    if _appendPath(filePathObj,
                                   doMatchIn,
                                   matchModeStrIn,
                                   matchStringsListIn,
                                   doIgnoreMatchIn,
                                   ignoreMatchModeStrIn,
                                   ignoreMatchStringsListIn):
                        # Yield the child directory
                        yield filePathObj

            # Do not continue to the child directories if this is not recurisve
            if not isRecursiveIn:
                break
            else:
                levelInt += 1
                if maxDepthIntIn > -1 and levelInt > maxDepthIntIn:
                    break

    def split(self):
        """
        Split the path

        Splits the path into a pair (head, tail) where tail is the base name
        and head is everything leading up to that

        Args:
            None

        Returns:
            (tuple): (str, str) Split FilePath
        """
        return os.path.split(self)

    def stringSplit(self,
                    splitCharacterStrIn="",
                    maxSplitIntIn=-1):
        """
        String Split

        Split the string by `splitCharacterStrIn` and return a list
        representation of the split string

        Args:
            None

        Keyword Args:
            splitCharacterStrIn (str): Character To Split the String By
            maxSplitIntIn (int): Max Split Number

        Returns:
            (list): Split String
        """
        return str.split(self,
                         splitCharacterStrIn,
                         maxSplitIntIn)

    def writeText(self,
                  testStrIn):
        """
        Writes the given `testStrIn` into the file path

        Args:
            testStrIn (str): Text to be written

        Returns:
            None
        """
        with self.openForWrite() as handleObj:
            handleObj.write(testStrIn)

    def asUnixPath(self):
        """
        Convert the path to a Unix Style FilePath (/ instead of \)

        Args:
            None

        Returns:
            (object): :class:`filepath\.FilePath` FilePath converted to Unix-style
        """
        return FilePath(self, pathTypeIntIn=FILEPATH_TYPE_UNIX)

    def asWindowsPath(self):
        """
        Convert the path to a Windows Style FilePath (\ instead of /)

        Args:
            None

        Returns:
            (object): :class:`filepath\.FilePath` FilePath converted to Windows-style
        """
        return FilePath(self, pathTypeIntIn=FILEPATH_TYPE_WINDOWS)

    def asMayaPath(self):
        """
        Convert the path to a Maya Style FilePath (UNIX Style) (\ instead of /)

        Args:
            None

        Returns:
            (object): :class:`filepath\.FilePath` FilePath converted to Maya-style
        """
        return FilePath(self, pathTypeIntIn=FILEPATH_TYPE_MAYA)

    def asDepotPath(self):
        """
        Convert the path to a Depot Style FilePath (//depot/lol instead of C:/depot/lol)

        Args:
            None

        Returns:
            (object): :class:`filepath\.FilePath` FilePath converted to Depot-style
        """
        return FilePath(self, pathTypeIntIn=FILEPATH_TYPE_DEPOT)


######################################
############# FUNCTIONS ##############
######################################
def DocumentPath():
    """
    Returns the Users "My Documents" FilePath

    Args:
        None

    Returns:
        (object): :class:`filepath\.FilePath` Users My Documents Folder
    """
    return HomePath().join("Documents")

def HomePath():
    """
    Returns the users Home FilePath

    Args:
        None

    Returns:
        (object): :class:`filepath\.FilePath` Users Home Folder
    """
    return FilePath(os.environ["USERPROFILE"])

def LocalAppDataPath():
    """
    Return the local app data path (Environment Variable `LOCALAPPDATA`)

    Args:
        None

    Returns:
        (object): :class:`filepath\.FilePath` Local App Data Folder
    """
    return FilePath(os.environ["LOCALAPPDATA"])

def PythonPaths():
    """
    Returns the list of python paths (Environment Variable `PYTHONPATH`)

    Args:
        None

    Returns:
        (list): List of :class:`filepath\.FilePath` Python Paths
    """
    pathsList = re.split("{0}+".format(os.pathsep), os.environ["PYTHONPATH"])
    return [FilePath(pathObj) for pathObj in pathsList]

def SystemPaths():
    """
    Returns the list of system paths (Environment Variable `PATH`)

    Args:
        None

    Returns:
        (object): :class:`filepath\.FilePath` System Paths
    """
    pathsList = re.split("{0}+".format(os.pathsep), os.environ["PATH"])
    return [FilePath(pathObj) for pathObj in pathsList]

def TempPath():
    """
    Returns the temp path (Environment Variable `TMP`)

    Args:
        None

    Returns:
        (object): :class:`filepath\.FilePath` Temp Folder
    """
    return FilePath(os.environ["TMP"])

def UserPath():
    """
    Returns the user path (Environment Variable `USERPROFILE`)

    Args:
        None

    Returns:
        (object): :class:`filepath\.FilePath` User Profile Folder
    """
    return FilePath(os.environ["USERPROFILE"])

def WindowsDir():
    """
    Returns the windows directory path (Environment Variable `WINDIR`)

    Args:
        None

    Returns:
        (object): :class:`filepath\.FilePath` Windows Directory Folder
    """
    return FilePath(os.environ["WINDIR"])

def ArtPath():
    """
    Returns the root art folder

    Args:
        None

    Returns:        
        (object): :class:`filepath\.FilePath`
    """
    return FilePath(os.environ.get('ART_PATH', 'C:\\'))

def GamePath():
    """
    Returns the root game folder

    Args:
        None

    Returns:     
        (object): :class:`filepath\.FilePath`
    """
    return FilePath(os.environ.get('GAME_PATH', 'C:\\'))

def UnrealPath():
    """
    Returns the root game folder

    Args:
        None

    Returns:     
        (object): :class:`filepath\.FilePath`
    """
    if os.environ.get('UNREAL_PATH', None):
        os.environ['UNREAL_PATH'] = FilePath(__file__).dir().dir().join('unreal_tools')
    return FilePath(os.environ.get('UNREAL_PATH', os.environ['UNREAL_PATH']))

def ExportPath(path):
    """
    Returns the combined export path from Artpath and Gamepath
    Args:
        None
    Returns: 
        (object): :class:`filepath\.FilePath`
    """ 
    return FilePath(FilePath(path).replace(ArtPath(), GamePath()))

def ToolsPath():
    """
    Returns the tool folder directory

    Args:
        None

    Returns:        
        (object): :class:`filepath\.FilePath`
    """
    return FilePath(os.environ['TOOLS_PATH'])

def IconPath():
    """
    Returns the icon folder directory

    Args:
        None

    Returns:        
        (object): :class:`filepath\.FilePath` Icon Folder
    """
    return FilePath(ToolsPath()).dir().join("icons")

def UserToolsPath():
    """
    Returns the User FilePath (document path + "UserToolsPath")

    Args:
        None

    Returns:
        (object): :class:`core.filepath.FilePath` UserToolsPath
    """
    return DocumentPath().join("ArtTools")


def MayaScenePath():
    """
    Returns the User FilePath (document path + "UserToolsPath")

    Args:
        None

    Returns:
        (object): :class:`core.filepath.FilePath` UserToolsPath
    """
    import maya.cmds as cmds
    return FilePath(cmds.file(q=True, sc=True))