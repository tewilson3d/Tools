"""
Perforce Library
"""
######################################
############# IMPORTS ################
######################################
import P4

import os
import stat
from time import sleep
import subprocess
import xml.etree.ElementTree as ET
import threading
import logging
import queue

import filepath
import singletons
import metaclasses


######################################
############# DEFINES ################
######################################
# Status Enums

#: Status Exists
STATUS_EXISTS = 1

#: Status Up To Date
STATUS_UP_TO_DATE = 2

#: Status Added
STATUS_ADDED = 4

#: Status Deleted
STATUS_DELETED = 8

#: Status Checked Out By Me
STATUS_CHECKED_OUT_ME = 16

#: Status Checked Out By Others
STATUS_CHECKED_OUT_OTHER = 32

#: Perforce Connection Timeout in Seconds
CONNECTION_TIMEOUT = 5

######################################
############# CLASSES ################
######################################
class PerforceWrapper(object):
    """
    Perforce Wrapper Object

    Notes:
        Any function that can directly call a perforce command, or calls an internal command that
        does so has a `argsListIn` argument. This is a magic argument that is used to pass
        additional command arguments to perforce.

        Each function has a link to its corresponding perforce command, view the additional
        documentation for a list of possible arguments

    Warning:
        When inheriting from this class DO NOT call init. An exception will be raised.  This class is using the singleton metaclass
        and is designed in such a way that inheriting from the base instance is possible. If the init were allowed to go through
        the base object attributes would be treated as their own unique instances, which will cause expected functionality to fail.

    Raises:
        (Exception): Exception raised when __init__ is called from an inherited class

    Attributes:
        p4Obj (object): :py:class:`P4.P4` Instance
        userStr (str): Perforce User
        clientStr (str): Perforce Client

    Keyword Args:
        clientStr (str): Perforce Client Override
    """
    __metaclass__ = metaclasses.classmaker(left_metas=(),
                                           right_metas=(metaclasses.BaseMetaClass, singletons.Singleton))

    #: Perforce instance
    p4Obj = None

    def __init__(self,
                 clientStr=None,
                 *argsListIn):

        # Check for inheritance calls
        if not isinstance(self, PerforceWrapper):
            raise Exception("Calling __init__ from an inherited singleton object is not allowed")

        # Create the Perforce Instance
        self.p4Obj = P4.P4()

        # Connect to Perforce
        self._connect()

        # Set the user
        self.userStr = self.p4Obj.user

        # Override client for the wrapper instance
        self._setClient(clientStr)

        # Set the Client
        self.clientStr = self.p4Obj.client

        # Read in user preferences
        self._getUserPreferences()

    ######## Properties ########

    @property
    def clientRoot(self):
        """
        Get the Client Root

        Args:
            None

        Returns:
            (str): Perforce Client Root

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> print PerforceWrapper().clientRoot

        """
        return self.info()[0]["clientRoot"]


    @property
    def clientHost(self):
        """
        Get the Client Host

        Args:
            None

        Returns:
            (str): Perforce Client Host

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> print PerforceWrapper().clientHost

        """
        return self.info()[0]["clientHost"]


    @property
    def clientName(self):
        """
        Get the Client Name

        Args:
            None

        Returns:
            (str): Perforce Client Name

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> print PerforceWrapper().clientName

        """
        return self.info()[0]["clientName"]


    @property
    def userName(self):
        """
        Get the User Name

        Args:
            None

        Returns:
            (str): Perforce User Name

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> print PerforceWrapper().userName

        """
        return self.info()[0]["userName"]


    @property
    def connected(self):
        """
        Get is Perforce Connected

        Args:
            None

        Returns:
            (bool): Perforce Connected
        """
        try:
            self._connect()
        except Exception as errorObj:
            return False

        return True

    @property
    def serverName(self):
        """
        Get Perforce Sever Name

        Args:
            None

        Returns:
            (str): Perforce Server Name

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> print PerforceWrapper().serverName

        """
        return self.info()[0]["serverAddress"]


    ######## Internals ########

    def __getattr__(self,
                    attrNameStrIn):
        """
        Get Attribute Override

        Args:
            attrNameStrIn (str): Attribute Name

        Returns:
            (void): Attribute Requested

        Raises:
            (AttributeError): Invalid Attribute Name
        """
        def interceptedFunctionCall(*argsListIn):
            """
            Intercepted Function Call

            Args:
                *argsListIn (tuple): Intercepted Function Calls

            Returns:
                (void): Dynamic Function Return
            """
            return self._runPerforceFunction(attrNameStrIn,
                                             *argsListIn)

        if attrNameStrIn.startswith("run_") or attrNameStrIn.startswith("fetch_") or attrNameStrIn.startswith("save_"):
            # This is a dynamic function call, return the interceptedFunctionCall
            # function
            return interceptedFunctionCall
        else:
            return object.__getattribute__(self,
                                           attrNameStrIn)


    def _runPerforceFunction(self,
                             functionNameStrIn,
                             *argsListIn):
        """
        Run the perforce function and return the result

        Args:
            functionNameStrIn (str): Perforce Function

        Returns:
            (void): Perforce Function Return
        """
        self._connect()

        # Get the function
        functionObj = getattr(PerforceWrapper().p4Obj,
                              functionNameStrIn)

        # Run the function
        return functionObj(*argsListIn)

    def _connect(self):
        """
        Connect to Perforce

        Args:
            None

        Returns:
            None
        """
        if isinstance(self.p4Obj, P4.P4):
            # Because the `connected` function is not reliable, we need to always
            # attempt to connect with timeout, which also verifys the connection
            # by calling the `run_info command`

            # Connect with timeout
            p4Obj = ConnectToPerforceWithTimeout(self.p4Obj)

            # Got a valid return
            if p4Obj is not None:
                self.p4Obj = p4Obj
            else:
                # Raise an exception pass through
                logging.error("Connection to Perforce Timed Out After {0} seconds".format(CONNECTION_TIMEOUT))


    def _disconnect(self):
        """
        Disconnect from Perforce

        Args:
            None

        Returns:
            None
        """
        if isinstance(self.p4Obj, P4.P4):
            # Are we connected?
            if self.p4Obj.connected():
                self.p4Obj.disconnect()


    def _convertToList(self,
                       itemsVoidIn):
        """
        Convert Items to a List

        Convert `itemsVoidIn` to a list

        Args:
            itemsVoidIn (void): (str/list) Item(s) to convert

        Returns:
            (list): Converted list
        """
        outFilesList = []

        # Convert string
        if isinstance(itemsVoidIn, str):
            outFilesList.append(itemsVoidIn)
        elif isinstance(itemsVoidIn, list):
            # Extend List
            outFilesList.extend(itemsVoidIn)
        elif isinstance(itemsVoidIn, tuple):
            outFilesList.extend(list(itemsVoidIn))

        return outFilesList

    def _appendFilesToList(self,
                           filesVoidIn,
                           filesListOut):
        """
        Appends `filesVoidIn` to `filesListOut` optionally fixing the casing

        Args:
            filesVoidIn (void): (list/str) File(s)
            filesListOut (list): List to append to

        Keyword Args:
            doCasingFixIn (bool): Fix the file casing

        Returns:
            None
        """
        # Check the argument
        if not isinstance(filesListOut, list):
            raise P4.P4Exception("Function argument 2 expected a list, got {0} instead".format(type(filesListOut)))

        # Convert the files to a list
        filesList = self._convertToList(filesVoidIn)

        return filesListOut.extend(filesList)


    def _convertPath(self,
                     filePathStrIn):
        """
        Get the absolute, lowercased path for `filePathStrIn`

        Args:
            filePathStrIn (str): File Path

        Returns:
            (str): Converted Path
        """
        # Return the depot path
        if filePathStrIn.startswith("//depot"):
            return filePathStrIn.lower()

        # Return the lowercased abs path
        return filepath.FilePath(filePathStrIn).absolutePath().lower()


    def _initFileStatus(self,
                        filePathStrIn):
        """
        Init a File Status Dictionary for `filePathStrIn`

        Args:
            filePathStrIn (str): File Path

        Returns:
            (dict): File Status
        """
        # Create the dictionary
        filePathDict = {
            "exists": False,
            "writeable": False,
            "sourceStatus": None,
            "error": None,
            "originalPath": filePathStrIn
        }

        # Return
        return filePathDict


    def _createStatusDict(self,
                          filePathsListIn):
        """
        Create a file status dictionary for `filePathsListIn`

        Args:
            filePathsListIn (list): List of File Paths

        Returns:
            (dict): Status Dictionary
        """
        # Inititialize the status dictionary
        statusDict = {}

        # Get the file paths
        filePathsList = self._convertToList(filePathsListIn)

        for filePathStr in filePathsList:
            # Convert the file path
            convertedFilePathStr = self._convertPath(filePathStr)

            # Add to the status dict
            statusDict[convertedFilePathStr] = self._initFileStatus(filePathStr)

        return statusDict


    def _generateChangelist(self,
                            changelistStrIn,
                            descriptionStrIn):
        """
        Utility Function to generate a changelist

        Args:
            changelistStrIn (str): Changelist Number
            descriptionStrIn (str): Changelist Description

        Returns:
            (str): Changelist Number
        """
        changelistStr = None

        # Determine if we are using an existing changelist or creating a new one
        if changelistStrIn is None:
            try:
                if descriptionStrIn is not None:
                    # Create the changelist
                    changelistStr = self.createChangelist(descriptionStrIn=descriptionStrIn)
                else:
                    # Create the changelist
                    changelistStr = self.createChangelist()
            except P4.P4Exception as errorObj:
                self._logErrors(errorObj)
                return None
        elif changelistStrIn is not None and descriptionStrIn is not None:
            changelistStr = self._modifyChangelistDescription(changelistStrIn, descriptionStrIn)
        else:
            changelistStr = changelistStrIn

        return changelistStr

    def _getUserPreferences(self):
        #Get path to p4 prefs
        applicationSettingsPath = str(filepath.FilePath( os.environ["userprofile"] ).join( [".p4qt","ApplicationSettings.xml"] ))

        # Pre-scan the data to remove the "applicationSettingsData" tag, since it contains binary data the parser doesn't like
        applicationSettingsStringToParse = ""
        with open(applicationSettingsPath, "r") as applicationSettingsFile:
            applicationSettingsData = applicationSettingsFile.readlines()

            for line in applicationSettingsData:
                if "UniqueUserIdForDataCollection" in line:
                    applicationSettingsData.remove(line)

            applicationSettingsStringToParse = "\n".join(applicationSettingsData)

        root = ET.fromstring(applicationSettingsStringToParse)

        #Find the program associated with diffing in P4
        for associations in root.findall("Associations"):
            if associations.attrib['varName'] == "DiffAssociations":
                #If it's external, pull those values
                if associations.find('RunExternal').text == "true":
                    for singleAssociation in associations.findall("Association"):
                        #Get default diff program (not currently supporting file specific diffs)
                        if singleAssociation.attrib['varName'] == "Default Association":
                            self._diffAppPath = singleAssociation.find('Application').text
                            self._diffArguments = singleAssociation.find('Arguments').text
                #Otherwise use the default P4 Diff
                else:
                    self._diffAppPath = "p4merge.exe"
                    self._diffArguments = "%1 %2"

    def _logErrors(self,
                   errorObjIn,
                   doRaiseExceptionIn=False,
                   doRaiseWarningsIn=False):
        """
        Log the perforce error and raise the exception

        Args:
            errorObjIn (P4.P4Exception): P4 Exception

        Keyword Args:
            doRaiseExceptionIn (bool): Raise Exception
            doRaiseWarningsIn (bool): Raise Exception on Warnings

        Returns:
            None

        Raises:
            (P4.P4Exception): Caught P4 Exception
        """
        # Log the errors
        for errorObj in self.p4Obj.errors:
            logging.error(errorObj)

        # Log the warnings
        for warningObj in self.p4Obj.warnings:
            logging.warning(warningObj)

        # Raise the exception, stop execution
        if doRaiseExceptionIn == True:
            if len(self.p4Obj.errors) > 0:
                for item in self.p4Obj.errors:
                    if item.split('\n', 1)[0] in self.p4ErrorToUserErrorList():
                        raise Exception(item, 'Error During P4 Operation')
                else:
                    raise errorObjIn

        # Raise the exception, stop execution
        if doRaiseWarningsIn == True:
            if len(self.p4Obj.warnings) > 0:
                for item in self.p4Obj.warnings:
                    if item.split('\n', 1)[0] in self.p4ErrorToUserErrorList():
                        raise Exception(item, 'Error During P4 Operation')
                else:
                    raise errorObjIn


    ######## Class Methods #########
    @classmethod
    def loggedIn(cls):
        """
        Determine if the user is logged in to P4

        Args:
            None

        Returns:
            (bool): Logged In To Perforce

        Raises:
            (P4.P4Exception): General P4 Exception
        """
        try:
            # Get the perforce instance
            p4Obj = PerforceWrapper()

            # Get the login info
            resultsStr = p4Obj.run_login("-s")

            # Logged in
            return True

        except P4.P4Exception as errorObj:
            p4Obj._logErrors(errorObj, False)

            # Not logged in
            return False

        # Not Logged in
        return False


    @classmethod
    def login(cls,
              passwordStrIn):
        """
        Log In To Perforce

        Args:
            passwordStrIn (str): Log In Password

        Returns:
            (bool): Successful Login
        """
        try:
            # Get the perforce instance
            p4Obj = PerforceWrapper()

            # Set the password
            p4Obj.p4Obj.password = str(passwordStrIn)

            # Run the login
            p4Obj.run_login()

            # Login was successfull
            return True
        except P4.P4Exception as errorObj:
            p4Obj._logErrors(errorObj,
                             doRaiseExceptionIn=False)

            # Failed to login
            return False

        # Failed to login
        return False


    ######## Public Methods ########
    def info(self,
             *argsListIn):
        """
        Returns the results from `p4 info`

        Gets and returns the results from the `p4 info` call

        p4 info <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_info.html>

        Args:
            None

        Returns:
            (list): P4 Info Results

        Raises:
            (P4.P4Exception): General P4 Exception

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 2

                >>> from general.perforce import PerforceWrapper
                >>> infoList = PerforceWrapper().info()
                >>> for keyStr, valueVoid in infoList[0].items():
                >>>     print "{0}:{1}".format(keyStr, valueVoid)

        """
        argList = []
        argList.extend(argsListIn)

        try:
            # Get the results
            infoList = self.run_info(*argList)

            # We might still be getting wrong data types here, we need to check before we return
            if isinstance(infoList, list):
                return infoList
            elif isinstance(infoList, bool):                
                raise Exception("Invalid Return Type! Expected list got bool")

        except P4.P4Exception as errorObj:
            # Log errors
            self._logErrors(errorObj)

    def where(self,
              filesVoidIn,
              *argsListIn):
        """
        Returns the results from `p4 where`

        Gets and returns the results from `p4 where`

        p4 where <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_where.html>

        Args:
            filesVoidIn (void): (list/str) File(s) to call `where` on

        Returns:
            (list): Mapped Files

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> whereListResults = PerforceWrapper().where("//depot/tools/art/python/core/general/perforce.py")
                >>> for keyStr, valueVoid in whereListResults[0].items():
                >>>     print "{0}:{1}".format(keyStr, valueVoid)

        """
        resultsList = []
        filesList = self._convertToList(filesVoidIn)

        for filePathObj in filesList:
            try:
                argList = []
                argList.append(filePathObj)
                argList.extend(argsListIn)

                # If there are multiple mappings for this file, return the last
                # entry that does not have an `unmap` key
                whereResultsList = self.run_where(*argList)

                # Add the result
                didAddResult = False

                if isinstance(whereResultsList, list) and len(whereResultsList) > 0:

                    for currentResultDict in reversed(whereResultsList):
                        if not currentResultDict.__contains__("unmap"):
                            resultsList.append(currentResultDict)
                            didAddResult = True

                            break

                    if didAddResult == False:
                        logging.warning("Warning: No mapped entry for {0} in user workspace".format(filePathObj))
                        resultsList.append(None)

                else:
                    resultsList.append(None)
            except P4.P4Exception as errorObj:
                resultsList.append(None)

                # Log the error
                self._logErrors(errorObj)

        return resultsList


    def files(self,
              filesVoidIn,
              *argsListIn):
        """
        Returns the results from `p4 files`

        Gets and returns the results from `p4 files`

        p4 files <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_filelog.html>

        Args:
            filesVoidIn (void): (list/str) File(s) to call `files` on

        Returns:
            (list): List of dictionaries containing file information

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> fileLogListResults = PerforceWrapper().files("//depot/tools/art/python/core/general/perforce.py")
                >>> for depotFileObj in fileLogListResults:
                >>>     print depotFileObj["depotFile"]
        """

        resultsList = None
        filesList = self._convertToList(filesVoidIn)

        argsList = []
        argsList.extend(argsListIn)
        argsList.extend(filesList)

        # Try go get files result
        try:
            badFilePathsList = []
            resultsList = self.run_files(*argsList)

        # If it fails, remove the bad paths and try again
        except P4.P4Exception as errorObj:
            # Go through the warnings and look for bad paths
            for currentWarningStr in self.p4Obj.warnings:
                # Looking for " - no such file(s)"
                warningSeperatorLocationInt = currentWarningStr.find(" - ")

                if warningSeperatorLocationInt >= 0:
                    badPathStr = currentWarningStr[0:warningSeperatorLocationInt]

                    if badPathStr in filesList:
                        badFilePathsList.append(badPathStr)
                    else:
                        logging.warning(
                            "[Perforce Status] Error - Unable to handle warning for: {0} {1}".format(badPathStr,
                                                                                                     currentWarningStr))

            # Go through the errors and look for bad paths
            for currentErrorStr in self.p4Obj.errors:
                # Get the bad path
                badPathList = currentErrorStr.split("'")

                if len(badPathList) > 1:
                    if badPathList[1] in filesList:
                        badFilePathsList.append(badPathList[1])
                    else:
                        logging.error(
                            "[Perforce Status] Error - Unable to handle error for: {0} {1}".format(badPathList[1],
                                                                                                   currentErrorStr))
                else:
                    logging.error("[Perforce Status] Error - Unable to handle error: {0}".format(currentErrorStr))

        # If the first pass fails, remove bad files and try second pass
        if resultsList is None:
            # Remove bad paths from the list
            filesList = list(set(filesList) - set(badFilePathsList))

            if len(filesList):
                # Try to get status again
                try:
                    resultsList = self.run_files(filesList)
                except P4.P4Exception as errorObj:
                    self._logErrors(errorObj, False)

                    # Second Pass Failed
                    return None

        return resultsList


    def have(self,
             fileStrIn,
             *argsListIn):
        """
        Calls the `p4 have` command for `fileStrIn`

        P4 Have <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_have.html>

        Args:
            fileStrIn (str): File To Check

        Returns:
            (list): Have Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> haveResultsList = PerforceWrapper().have("//depot/tools/art/python/core/general/perforce.py")
                >>> for keyStr, valueVoid in haveResultsList[0].items():
                >>>     print "{0}:{1}".format(keyStr, valueVoid)

        """
        resultsList = []

        try:
            argsList = [fileStrIn]
            argsList.extend(argsListIn)

            # Get the have result
            resultsList = self.run_have(*argsList)

        except P4.P4Exception as errorObj:
            # Log the error
            self._logErrors(errorObj)

            return None

        return resultsList

    def getPendingChangelists(self):
        """
        Get the pending changelists using `p4 changes`

        P4 Changes <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_changes.html>

        Args:
            None

        Returns:
            (list): Pending Changelists

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> pendingChangelistList = PerforceWrapper().getPendingChangelists()
                >>> for keyStr, valueVoid in pendingChangelistList[0].items():
                >>>     print "{0}:{1}".format(keyStr, valueVoid)

        """
        # Results
        resultsList = []

        # Get the P4 Info
        p4InfoList = self.info()

        if len(p4InfoList) > 0:
            p4InfoDict = p4InfoList[0]

            argList = ["-s",
                       "pending",
                       "-u",
                       p4InfoDict["userName"],
                       "-c",
                       p4InfoDict["clientName"],
                       "-l"]
            try:
                resultsList = self.run_changes(*argList)
            except P4.P4Exception as errorObj:
                self._logErrors(errorObj)

        return resultsList

    def createChangelist(self,
                          descriptionStrIn="Created By Python",
                         filesVoidIn=None,
                         doReuseExistingIn=False):
        """
        Create a new Perforce Changelist using `p4 change`

        P4 Change <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_change.html>

        Args:
            None

        Keyword Args:
            descriptionStrIn (str): Changelist Description
            filesVoidIn (void): (list/str) File(s) to add to the changelist
            doReuseExistingIn (bool): Reuse Existing Changelist

        Returns:
            (str): Created Changelist Number

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 4

                >>> from general.perforce import PerforceWrapper
                >>> createdChangelistStr = PerforceWrapper().createChangelist("New Changelist")
                >>> print createdChangelistStr
                >>> PerforceWrapper().deleteChangelist(createdChangelistStr)

        """
        # Reuse Changelist?
        if doReuseExistingIn:
            # Search for a changelist matching the description
            existingChangelistList = self._getPendingChangelists()

            for currentChangelistDict in existingChangelistList:
                if currentChangelistDict["desc"].strip() == descriptionStrIn:
                    return currentChangelistDict["change"]

        # Get the files
        filesList = self._convertToList(filesVoidIn)

        if len(filesList) > 0:
            filesList = self.where(filesList)

        # Create the dictionary
        changelistDict = {"Status":"new",
                          "Files":filesList,
                          "Description":str(descriptionStrIn),
                          "Client":self.clientName,
                          "User":self.userName,
                          "Change":"new"}

        # Create the changelist
        resultsList = self.save_change(changelistDict)

        # Get the changelist number
        if len(resultsList) > 0:
            changelistNumberStr = resultsList[0].split(" ")[1]
            return changelistNumberStr

        return ""

    def add(self,
             filesVoidListIn,
             changelistStrIn=None,
             doCasingFixIn=True,
             *argsListIn):
        # Convert to a list
        filesList = self._convertToList(filesVoidListIn)

        resultsList = []
        argsList = []

        # Ensure everything is under the p4 root
        whereResults = self.where(filesList)

        idxToPop = []
        for idx, result in enumerate(whereResults):
            if result is None:
                badPath = filesList[idx]
                idxToPop.append(idx)
                resultsList.append( "{0} - Can't add files outside of P4 Root".format(badPath) )

        # We reverse the list of indicies, so that we pop from high to low
        for idx in reversed(idxToPop):
            filesList.pop(idx)

        # Check out files into an existing changelist
        if changelistStrIn is not None:
            argsList = ["-c", changelistStrIn]

        # Append the files to the list
        self._appendFilesToList(filesList,
                                argsList)

        argsList.extend(argsListIn)

        # P4 Add
        try:
            addResults = self.run_add(*argsList)

        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)
        else:
            resultsList.extend(addResults)

        return resultsList


    def workspace(self,
                  *argsListIn):
        """
        Get the client workspace info

        P4 Workspace <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_workspace.html>

        Args:
            None

        Returns:
            (dict): Client Workspace

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 2

                >>> from general.perforce import PerforceWrapper
                >>> workspaceDict = PerforceWrapper().workspace()
                >>> for key, value in workspaceDict.items():
                >>>     print "{0}:{1}".format(key, value)

        """
        resultsDict = {}

        # Get the workspace
        argList = []
        argList.extend(argsListIn)

        try:
            resultsDict = self.fetch_workspace(*argList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsDict

    def delete(self,
                filesVoidIn,
               changelistStrIn=None,
               *argsListIn):
        """
        Run `p4 delete` on `filesVoidIn`

        P4 Delete <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_delete.html>

        Args:
            filesVoidIn (void): (list/str) File(s) to delete

        Keyword Args:
            changelistStrIn (str): Changelist Number

        Returns:
            (list): Delete Results

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 3

                >>> from general.perforce import PerforceWrapper
                >>> deleteResultList = PerforceWrapper().delete("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> PerforceWrapper().revert("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> for key, value in deleteResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        resultsList = []
        argsList = []

        # Delete files into an existing changelist
        if changelistStrIn is not None:
            argsList = ["-c", changelistStrIn]

        # Append files to the list
        self._appendFilesToList(filesList,
                                argsList)

        argsList.extend(argsListIn)

        # Delete
        try:
            resultsList = self.run_delete(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList

    def edit(self,
              filesVoidIn,
             changelistStrIn=None,
             *argsListIn):
        """
        Run `p4 edit` on `filesVoidIn`

        P4 Edit <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_edit.html>

        Args:
            filesVoidIn (void): (list/str) File(s) to Edit

        Keyword Args:
            changelistStrIn (str): Changelist Number

        Returns:
            (list): Edit Results

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 3

                >>> from general.perforce import PerforceWrapper
                >>> editResultList = PerforceWrapper().edit("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> PerforceWrapper().revert("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> for key, value in editResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        resultsList = []
        argsList = []

        # Check out files into an existing changelist
        if changelistStrIn is not None:
            argsList = ["-c", changelistStrIn]

        # Append to list
        self._appendFilesToList(filesList,
                                argsList)

        argsList.extend(argsListIn)

        # Edit Files
        try:
            resultsList = self.run_edit(*argsList)

        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList

    def resolve(self,
                filesVoidIn,
                *argsListIn):
        """
        Run `p4 resolve` on `filesVoidIn`

        P4 resolve <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_resolve.html>

        Args:
            filesVoidIn (void): (list/str) File(s) to Resolve
            argsListIn (list): Resolve Arguments

        Returns:
            (list): Resolve Results

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 2

                >>> from general.perforce import PerforceWrapper
                >>> PerforceWrapper().edit("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> resolveResultList = PerforceWrapper().resolve("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt", ["-Ac"])
                >>> print resolveResultList

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        resultsList = []

        # With lists being a mutable type and `_appendFilesToList` directly editing the list
        # I think it's safer to create a new list to edit rather than directly edit the input argument
        argsList = []
        argsList.extend(argsListIn)

        # Append files
        self._appendFilesToList(filesList,
                                argsList)

        # Resolve
        try:
            resultsList = self.run_resolve(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList


    def revert(self,
               filesVoidIn,
               isTestIn=False,
               revertUnchangedIn=False,
               changelistStrIn=None,
               *argsListIn):
        """
        Run `p4 revert` on `filesVoidIn`

        P4 Revert <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_revert.html>

        Args:
            filesVoidIn (void): (list/str) File(s) to revert

        Keyword Args:
            isTestIn (bool): Only Print Files that would revert
            doForceIn (bool): Forces Revert of Changed Files
            changelistStrIn (str): Changelist to revert from

        Returns:
            (list): Revert Results

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 2

                >>> from general.perforce import PerforceWrapper
                >>> PerforceWrapper().edit("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> revertResultList = PerforceWrapper().revert("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> for key, value in revertResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """

        resultsList = []
        argsList = []

        # Test Mode
        if isTestIn == True:
            argsList = ["-n"]

        # Force
        if revertUnchangedIn == True:
            argsList.extend(["-a"])

        # Changelist
        if changelistStrIn is not None:
            argsList.extend(["-c",
                             changelistStrIn])

        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        # Append files
        self._appendFilesToList(filesList,
                                argsList)

        argsList.extend(argsListIn)


        # Revert
        try:
            resultsList = self.run_revert(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList

    def fstat(self,
               filesVoidIn,
              *argsListIn):
        """
        Run `p4 fstat` on `filesVoidIn`

        P4 Fstat <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_fstat.html>

        Args:
            filesVoidIn (void): (list/str) File(s) to run fstat on

        Returns:
            (list): Fstat Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> fstatResultList = PerforceWrapper().fstat("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> for key, value in fstatResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Convert to a list
        filePathsList = self._convertToList(filesVoidIn)

        argsList = []
        argsList.append(filePathsList)
        argsList.extend(argsListIn)

        resultsList = None
        badFilePathsList = []

        # Run Fstat
        try:
            resultsList = self.run_fstat(*argsList)
        except P4.P4Exception as errorObj:
            # Go through the warnings and look for bad paths
            for currentWarningStr in self.p4Obj.warnings:
                # Looking for " - no such file(s)"
                warningSeperatorLocationInt = currentWarningStr.find(" - ")

                if warningSeperatorLocationInt >= 0:
                    badPathStr = currentWarningStr[0:warningSeperatorLocationInt]

                    if badPathStr in filePathsList:
                        badFilePathsList.append(badPathStr)
                    else:
                        logging.warning("[Perforce Status] Error - Unable to handle warning for: {0} {1}".format(badPathStr,
                                                                                                                 currentWarningStr))

            # Go through the errors and look for bad paths
            for currentErrorStr in self.p4Obj.errors:
                # Get the bad path
                badPathList = currentErrorStr.split("'")

                if len(badPathList) > 1:
                    if badPathList[1] in filePathsList:
                        badFilePathsList.append(badPathList[1])
                    else:
                        logging.error("[Perforce Status] Error - Unable to handle error for: {0} {1}".format(badPathList[1],
                                                                                                             currentErrorStr))
                else:
                    logging.error("[Perforce Status] Error - Unable to handle error: {0}".format(currentErrorStr))

        # If the first pass fails, remove bad files and try second pass
        if resultsList is None:
            # Remove bad paths from the list
            filePathsList = list(set(filePathsList) - set(badFilePathsList))

            if len(filePathsList):
                # Try to get status again
                try:
                    resultsList = self.run_fstat(filePathsList)
                except P4.P4Exception as errorObj:
                    self._logErrors(errorObj, False)

                    # Second Pass Failed
                    return None

        # Weird edge case where somehow fstat returns false instead of None
        if isinstance(resultsList, bool):
            return None

        return resultsList


    def rollback(self,
                 filesWithRevisionsVoidIn):
        """
        Rollback Edited Files

        Rollback `filesWithRevisionsVoidIn` using `p4 sync`, `p4 edit`, and `p4 resolve`

        Args:
            filesWithRevisionsVoidIn (void): (list/str) File(s) To Rollback

        Returns:
            (str): Rollback Changelist - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 3, 4

                >>> from general.perforce import PerforceWrapper
                >>> rollbackChangelistStr = PerforceWrapper().rollback("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> PerforceWrapper().revert("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> PerforceWrapper().deleteChangelist(rollbackChangelistStr)
                >>> print rollbackChangelistStr

        """
        # Convert to a list
        filesWithRevisionsList = self._convertToList(filesWithRevisionsVoidIn)

        # Get the File Statues
        fileStatusesList = self.fstat(filesWithRevisionsList)

        # Rollback Data
        editedFilesList = []
        addedFilesList = []
        deletedFilesList = []

        # Go through the file statues
        for statusDict in fileStatusesList:
            # Get the previous version
            previousVersionInt = int(statusDict["headRev"])-1

            # Get the rollback status
            headActionStr = statusDict["headAction"]

            if headActionStr == "edit":
                editedFilesList.append((statusDict["depotFile"],
                                        previousVersionInt))
            elif headActionStr == "delete":
                deletedFilesList.append((statusDict["depotFile"],
                                         previousVersionInt))
            elif headActionStr == "add":
                addedFilesList.append((statusDict["depotFile"],
                                       previousVersionInt))

        # Skip if we have nothing to rollback
        if len(editedFilesList) == 0 and len(addedFilesList) == 0 and len(deletedFilesList) == 0:
            return

        # Create the changelist
        changelistStr = self.createChangelist("Rolling back files via Python Lib")

        # Rollback edited files
        if len(editedFilesList) > 0:
            # Previous Revisioned Path
            previousRevisionedPathsList = []

            filesList = []

            for infoDict in editedFilesList:
                previousRevisionedPathsList.append("{0}#{1}".format(infoDict[0], infoDict[1]))
                filesList.append(infoDict[0])

            # Roll Back
            self.sync(previousRevisionedPathsList)
            self.edit(filesList,
                       changelistStrIn=changelistStr)
            self.sync(filesList)
            self.resolve(filesList,
                         ["-ay"])

        # Rollback deleted files
        if len(deletedFilesList) > 0:
            previousRevisionedPathsList = []
            filesList = []

            for infoDict in deletedFilesList:
                previousRevisionedPathsList.append("{0}#{1}".format(infoDict[0], infoDict[1]))
                filesList.append(infoDict[0])

            # Roll Back
            self.sync(previousRevisionedPathsList)
            self.add(filesList,
                      changelistStrIn=changelistStr)


        # Rollback added files
        if len(addedFilesList) > 0:
            filesList = []

            for infoDict in addedFilesList:
                filesList.append(infoDict[0])

            # Rollback
            self._delete(filesList,
                         changelistStrIn=changelistStr)

        return changelistStr


    def move(self,
             fromFileStrIn,
             toFileStrIn,
             changelistStrIn=None,
             *argsListIn):
        """
        Run `p4 move` from `fromFileStrIn` to `toFileStrIn`

        P4 Move <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_move.html>

        Args:
            fromFileStrIn (str): File to Move
            toFileStrIn (str): File To Move To

        Keyword Args:
            changelistStrIn (str): Changelist Number

        Returns:
            (list): Move Results - Note: Returns None if Exception Encountered


        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 2, 3

                >>> from general.perforce import PerforceWrapper
                >>> PerforceWrapper().edit("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> moveResultsList = PerforceWrapper().move("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt", "//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_2.txt")
                >>> PerforceWrapper().revert(["//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt", "//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_2.txt"])
                >>> for key, value in moveResultsList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        resultsList = None
        argsList = []

        # Check out files into an existing changelist
        if changelistStrIn is not None:
            argsList = ["-c", changelistStrIn]

        # Add the move arguments
        argsList.extend([fromFileStrIn, toFileStrIn])

        argsList.extend(argsListIn)

        # Get the results
        try:
            resultsList = self.run_move(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList

    def sync(self,
              filesVoidIn,
             *argsListIn,
             **keywordArgsListIn):
        """
        Run `p4 sync` on `filesVoidIn`

        P4 Sync <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_move.html>

        Args:
            filesVoidIn (void): (list/str) File(s) to sync

        Returns:
            (list): Sync Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 2

                >>> from general.perforce import PerforceWrapper
                >>> PerforceWrapper().run_sync("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt#1")
                >>> syncResultList = PerforceWrapper().sync("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> for key, value in syncResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        resultsList = None

        # Keyword Arguments
        doRaiseErrors = keywordArgsListIn.get("raiseErrors", False)
        doRaiseWarnings = keywordArgsListIn.get("raiseWarnings", False)

        # Get a file list
        filesList = self._convertToList(filesVoidIn)

        """
        In order to make the p4_sync return useful info, it can't be run on any specific files that
        are already at the head revision. It's stupid that we have to do this, but we first check
        for any non-wildcard files and remove them from the list if they're already synced.
        (Note that it doesn't make sense if force flag is passed in, so we skip this step)
        """
        if "-f" not in argsListIn:
            nonWildFilesList = []

            for filePathStr in filesList:
                # Add Non-Wildcard Files
                if "..." not in filePathStr and "*" not in filePathStr:
                    nonWildFilesList.append(filePathStr)

            if len(nonWildFilesList) > 0:
                fileStatusDict = self.status(nonWildFilesList)

                if fileStatusDict is not None:
                    for filePathStr, statusDict in fileStatusDict.items():
                        if statusDict is not None and statusDict["sourceStatus"] is not None:
                            if statusDict["sourceStatus"]["up_to_date"]:
                                filesList.remove(filePathStr)

        # Done if all files removed
        if len(filesList) == 0:
            return resultsList

        # Build the arglist
        argsList = []
        argsList.append(filesList)
        argsList.extend(argsListIn)

        # Try to run the sync
        try:
            resultsList = self.run_sync(argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj,
                            doRaiseErrors,
                            doRaiseWarnings)

        return resultsList

    def diff(self,
              filesVoidIn,
             *argsListIn):
        """
        Diff Files using `p4 diff`

        P4 Diff <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_diff.html>

        Args:
            filesVoidIn (void): (str/list) Files to diff

        Returns:
            (list): Diff Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 4

                >>> from general.perforce import PerforceWrapper
                >>> PerforceWrapper().checkout("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> diffResultList = PerforceWrapper().diff(["//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt", "//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt"])
                >>> PerforceWrapper().revert("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> for key, value in diffResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Results
        resultsList = None

        # Build the arguments
        argsList = []
        argsList.extend(argsListIn)

        # Convert to a list
        self._appendFilesToList(filesVoidIn, argsList)

        try:
            resultsList = self.run_diff(*argsList)

        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList


    def diffGui(self,
                filesVoidIn):
        """
        Use `p4 diff` to launch and display differences in the chosen P4 diff application

        P4 Diff <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_diff.html>

        Args:
            filesVoidIn (void): (str/list) Files to diff

        Returns:
            (void): Returns None

        Examples:


        """
        # Build the arguments
        argsList = []

        # Convert to a list
        self._appendFilesToList(filesVoidIn, argsList)

        #This is a "dumb" solution, but to get p4 diff to open the GUI you need to set this env variable
        #The p4python set functions weren't working for me, so I went to system calls

        #First set the P4DIFF to the path to the diff app that we determined at setup
        subprocess.call('p4 set P4DIFF="{0}"'.format(self._diffAppPath) )

        for filePath in filesVoidIn:
            #Then run the diff command to launch the GUI. We do this via popen so the app won't hang while the diff is up
            subprocess.Popen("p4 diff {0}".format( filePath ))

        #Give the diff time to launch before unsetting the P4DIFF env variable
        sleep(1)
        subprocess.call('p4 set P4DIFF=' )


    def syncDir(self,
                directoryStrIn,
                *argsListIn):
        """
        Sync a directory using `p4 sync`

        P4 Sync <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_sync.html>

        Args:
            directoryStrIn (str): Directory to sync

        Returns:
            (list): Sync Dir Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 2

                >>> from general.perforce import PerforceWrapper
                >>> PerforceWrapper().run_sync("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt#1")
                >>> syncDirResultList = PerforceWrapper().syncDir("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/")
                >>> for key, value in syncDirResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Results
        resultsList = None

        # Arguments
        argsList = ["{0}...#head".format(directoryStrIn)]
        argsList.extend(argsListIn)

        # Sync
        try:
            resultsList = self.run_sync(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList


    def dirs(self,
             directoryStrIn,
             *argsListIn):
        """
        Get Immediate Sub Directories of directoryStrIn using `p4 dirs`

        P4 Dirs <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_dirs.html>

        Args:
            directoryStrIn (str): Directory To Get Sub Directories

        Returns:
            (list): Dirs Result - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> dirsResultList = PerforceWrapper().dirs("//depot/tools/art/python/UnitTests/unitTestModules/Core/data")
                >>> for key, value in dirsResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Results
        resultsList = None

        # Args
        argsList = []
        argsList.extend(argsListIn)

        # Add the directory
        argsList.append("{0}/*".format(directoryStrIn))

        try:
            resultsList = self.run_dirs(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList


    def statusDir(self,
                  directoryStrIn,
                  *argsListIn):
        """
        Get the status for a directory using `p4 fstat`

        P4 Fstat <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_fstat.html>

        Args:
            directoryStrIn (str): Directory to retrieve status of

        Returns:
            (list): Status Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> statusDirResult = PerforceWrapper().statusDir("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/")
                >>> for key, value in statusDirResult[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Results
        resultsList = None

        # Args
        argsList = ["{0}...#head".format(directoryStrIn)]
        argsList.extend(argsListIn)

        try:
            resultsList = self.run_fstat(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList


    def shortenP4Status(self,
                        sourceStatusDictIn):
        """
        Shorten a P4 Status

        Args:
            sourceStatusDictIn (dict): P4 Status to shorten

        Returns:
            (str): Shortened P4 Status

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> p4StatusDict = PerforceWrapper().status("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> shortenedP4StatusStr = PerforceWrapper().shortenP4Status(p4StatusDict)
                >>> print shortenedP4StatusStr

        """
        # Local File
        if sourceStatusDictIn is None:
            return "Local File"

        # Make sure we have the correct keys
        if "otherCheckOut" not in sourceStatusDictIn:
            return "Local File"

        if "addedByMe" not in sourceStatusDictIn:
            return "Local File"

        if "checkedOutByMe" not in sourceStatusDictIn:
            return "Local File"

        if "fstat" not in sourceStatusDictIn:
            return "Local File"

        if "up_to_date" not in sourceStatusDictIn:
            return "Local File"

        # Other Checkout
        elif len(sourceStatusDictIn["otherCheckOut"]) > 0:
            personStr = sourceStatusDictIn["otherCheckOut"][0].split("@")[0]
            return "Other {0}".format(personStr.title())

        # Added By Me
        elif sourceStatusDictIn["addedByMe"]:
            return "Add"

        # Checked Out By Me
        elif sourceStatusDictIn["checkedOutByMe"]:
            return "Edit"

        # Delete
        elif (sourceStatusDictIn["fstat"].__contains__("action") and
              sourceStatusDictIn["fstat"]["action"] == "delete"):
            return "Delete"

        # Out of Date
        elif not sourceStatusDictIn["up_to_date"]:
            return "Out of Date"

        # Unknown Status
        else:
            return ""

    def status(self,
               filePathsVoidIn,
               *argsListIn):
        """
        Build a status dictionary using :func:`PerforceWrapper.fstat`

        Args:
            filePathsVoidIn (void): (list/str) File Path(s)

        Returns:
            (dict): File Statuses

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> p4StatusDict = PerforceWrapper().status("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> for key, value in p4StatusDict.items():
                >>>     print "\t{0}".format(key)
                >>>     for subKey, subValue in value.items():
                >>>         if subKey == "sourceStatus":
                >>>             print "\tsourceStatus"
                >>>             for statusKey, statusValue in subValue.items():
                >>>                 if statusKey == "fstat":
                >>>                     print "\t\tfstat"
                >>>                     for fstatKey, fstatValue in statusValue.items():
                >>>                         print "\t\t\t{0}:{1}".format(fstatKey, fstatValue)
                >>>                 else:
                >>>                     print "\t\t{0}:{1}".format(statusKey, statusValue)
                >>>         else:
                >>>             print "\t{0}:{1}".format(subKey, subValue)


        """
        # Convert to a list
        filePathsList = self._convertToList(filePathsVoidIn)

        # Create a status dict
        statusDict = self._createStatusDict(filePathsList)

        newFilePathsList = list(statusDict.keys())

        argsList = []
        argsList.append(newFilePathsList)
        argsList.extend(argsListIn)

        # Get the fstat
        fstatsList = self.fstat(*argsList)

        if fstatsList is not None and isinstance(fstatsList, (list, tuple, dict)):
            statusDictFilesList = statusDict.keys()

            # Loop through the results
            for currentResultDict in fstatsList:
                # Get the client file
                clientFileStr = self._convertPath(currentResultDict["clientFile"])

                if clientFileStr not in statusDictFilesList:
                    clientFileStr = currentResultDict["depotFile"].lower()

                    if clientFileStr.lower() not in statusDictFilesList:
                        logging.error("Bad: {0}".format(currentResultDict["clientFile"]))
                        logging.error("[Perforce Status] Error - Unable to process: {0}".format(clientFileStr))
                        return None


                # Build the status dict
                statusDict[str(clientFileStr)]["sourceStatus"] = {
                    "fstat": currentResultDict,
                    "localVersion": -1,
                    "headVersion": -1,
                    "checkedOutByMe": False,
                    "addedByMe": False,
                    "up_to_date": True,
                    "deleted": False,
                    "changeList": -1,
                    "otherCheckOut": []
                }

                # Local Dictionary
                localStatusDict = statusDict[clientFileStr]["sourceStatus"]

                # Have Rev
                if "haveRev" in currentResultDict:
                    localStatusDict["localVersion"] = currentResultDict["haveRev"]

                # Head Rev
                if "headRev" in currentResultDict:
                    localStatusDict["headVersion"] = currentResultDict["headRev"]

                # Determine if up to date
                if "headRev" in currentResultDict and "haveRev" in currentResultDict:
                    if currentResultDict["haveRev"] != currentResultDict["headRev"]:
                        localStatusDict["up_to_date"] = False
                elif "headRev" in currentResultDict and "headAction" in currentResultDict:
                    if currentResultDict["headAction"] == "delete" or currentResultDict["headAction"] == "move/delete":
                        localStatusDict["deleted"] = True
                    else:
                        localStatusDict["up_to_date"] = False

                # Action
                if "action" in currentResultDict:
                    # Edit
                    if currentResultDict["action"] == "edit":
                        localStatusDict["checkedOutByMe"] = True
                    # Add
                    elif currentResultDict["action"] == "add":
                        localStatusDict["addedByMe"] = True

                # Change
                if "change" in currentResultDict:
                    localStatusDict["changeList"] = currentResultDict["change"]

                # Other Open
                if "otherOpen" in currentResultDict:
                    localStatusDict["otherCheckOut"] = currentResultDict["otherOpen"]

        # New Status Dict
        newStatusDict = {}
        for keyStr in statusDict.keys():
            # Build the Dictionary
            originalPathStr = statusDict[keyStr]["originalPath"]
            newStatusDict[originalPathStr] = statusDict[keyStr]
            newStatusDict[originalPathStr]["convertedPath"] = keyStr
            newStatusDict[originalPathStr].pop("originalPath")

            # Build the path
            filePathStr = originalPathStr

            if originalPathStr.startswith("//"):
                filePathStr = None
                if newStatusDict[originalPathStr]["sourceStatus"] is not None:
                    filePathStr = newStatusDict[originalPathStr]["sourceStatus"]["fstat"]["clientFile"]

            if filePathStr is not None:
                if os.path.exists(filePathStr):
                    newStatusDict[originalPathStr]["exists"] = True

                    if os.access(filePathStr, os.W_OK):
                        newStatusDict[originalPathStr]["writeable"] = True

        return newStatusDict

    def quickStatus(self,
                     filePathsVoidIn,
                    *argsListIn):
        """
        Returns a dictionary of file statuses with (key, value) == (filePath, statusEnum)

        Args:
            filePathsVoidIn (void): (list/str) File Path(s)

        Returns:
            (dict): Status Dictionary

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> p4QuickStatusDict = PerforceWrapper().quickStatus("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> for key, value in p4QuickStatusDict.items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Convert to a list
        filePathsList = self._convertToList(filePathsVoidIn)

        # Status Dictionary
        outStatusDict = {}

        argsList = []
        argsList.append(filePathsList)
        argsList.extend(argsListIn)

        # Get the status
        statusDict = self.status(*argsList)

        if statusDict is not None:
            for filePathStr in filePathsList:
                outStatusDict[filePathStr] = 0

                # In Perforce
                if filePathStr in statusDict:
                    if statusDict[filePathStr]["sourceStatus"]:
                        # Exists
                        outStatusDict[filePathStr] |= STATUS_EXISTS

                        # File up to date
                        if statusDict[filePathStr]["sourceStatus"]["up_to_date"]:
                            outStatusDict[filePathStr] |= STATUS_UP_TO_DATE

                        # Added
                        if statusDict[filePathStr]["sourceStatus"]["addedByMe"]:
                            outStatusDict[filePathStr] |= STATUS_ADDED

                        # Deleted
                        elif statusDict[filePathStr]["sourceStatus"]["deleted"]:
                            outStatusDict[filePathStr] |= STATUS_DELETED

                        # Checked out by this user
                        if statusDict[filePathStr]["sourceStatus"]["checkedOutByMe"]:
                            outStatusDict[filePathStr] |= STATUS_CHECKED_OUT_ME

                        # Checked out by others
                        elif statusDict[filePathStr]["sourceStatus"]["otherCheckOut"]:
                            outStatusDict[filePathStr] |= STATUS_CHECKED_OUT_OTHER

        return outStatusDict


    def isLocked(self,
                 filesPathVoidIn):
        """
        Returns a Bool or List (depending on `filesPathVoidIn` type) denoting if the file(s) is/are 
        locked

        Args:
            filesPathVoidIn (void): (list/str) File Path(s)

        Returns:
            (bool/list[bools]): Files Locked

        Examples:

        .. runblock:: pycon
        :hidden-statements: 1

        >>> from general.perforce import PerforceWrapper
        >>> isLocked = PerforceWrapper().isLocked("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
        >>> print isLocked
        """
        # Convert to a list
        filePathsList = self._convertToList(filesPathVoidIn)

        # Get the status for the files
        fstatList = self.fstat(filePathsList)

        # Fstat failed somewhere - at least we know the file is not locked
        if fstatList is None:
            return False

        # Locked List
        lockedList = []

        for fstatDict in fstatList:
            if "otherLock" in fstatDict or "ourLock" in fstatDict:
                lockedList.append(True)
            else:
                lockedList.append(False)

        if hasattr(filesPathVoidIn, "__iter__"):
            return lockedList
        else:
            return lockedList[0]		


    def isOutOfDate(self,
                    filesPathVoidIn):
        """
        Returns a Bool or List (depending on `filesPathVoidIn` type) denoting if the file(s) are
        out of date

        Args:
            filesPathVoidIn (void): (list/str) File Path(s)

        Returns:
            (bool/list[bools]): Files out of date

        Examples:

        .. runblock:: pycon
        :hidden-statements: 1

        >>> from general.perforce import PerforceWrapper
        >>> isOutOfDate = PerforceWrapper().isOutOfDate("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
        >>> print isOutOfDate	    
        """
        # Convert to a list
        filePathsList = self._convertToList(filesPathVoidIn)

        # Get the status for the files
        quickStatusDict = self.quickStatus(filePathsList)

        # Out of Date List
        outOfDateList = []

        for filePathStr in filePathsList:
            if not (quickStatusDict[filePathStr] & STATUS_UP_TO_DATE):
                outOfDateList.append(True)
            else:
                outOfDateList.append(False)

        if hasattr(filesPathVoidIn, "__iter__"):
            return outOfDateList
        else:
            return outOfDateList[0]


    def isCheckedOut(self,
                     filesPathVoidIn):
        """
        Returns a Bool or List (depending on `filesPathVoidIn` type) denoting if the file(s) are
        checked out

        Args:
            filesPathVoidIn (void): (list/str) File Path(s)

        Returns:
            (bool/list[bools]): Files checked out

        Examples:

        .. runblock:: pycon
        :hidden-statements: 1

        >>> from general.perforce import PerforceWrapper
        >>> isCheckedOut = PerforceWrapper().isCheckedOut("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
        >>> print isCheckedOut	  	    
        """
        # Convert to a list
        filePathsList = self._convertToList(filesPathVoidIn)

        # Get the status for the files
        quickStatusDict = self.quickStatus(filePathsList)

        # Checked Out List
        checkedOutList = []

        for filePathStr in filePathsList:
            if (quickStatusDict[filePathStr] & STATUS_CHECKED_OUT_ME) \
               or (quickStatusDict[filePathStr] & STATUS_CHECKED_OUT_OTHER):
                checkedOutList.append(True)
            else:
                checkedOutList.append(False)

        if hasattr(filesPathVoidIn, "__iter__"):
            return checkedOutList
        else:
            return checkedOutList[0]        


    def needsAdd(self,
                 filesPathVoidIn):
        """
        Returns a Bool or List (depending on `filesPathVoidIn` type) denoting if the file(s) are
        need to be added

        Args:
            filesPathVoidIn (void): (list/str) File Path(s)

        Returns:
            (bool/list[bools]): Files need add

        Examples:

        .. runblock:: pycon
        :hidden-statements: 1

        >>> from general.perforce import PerforceWrapper
        >>> needsAdd = PerforceWrapper().needsAdd("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
        >>> print needsAdd	    
        """
        # Convert to a list
        filePathsList = self._convertToList(filesPathVoidIn)

        # Get the status for the files
        quickStatusDict = self.quickStatus(filePathsList)

        # Needs add List
        needsAddList = []

        for filePathStr in filePathsList:
            # Ensure we have a local path
            localPathList = self.getLocalPaths(filePathStr)

            if len(localPathList) == 0:
                needsAddList.append(True)
                continue

            localPathStr = localPathList[0]

            if localPathStr is not None and os.path.exists(localPathStr):
                if quickStatusDict[filePathStr] == 0:
                    needsAddList.append(True)
                else:
                    needsAddList.append(False)
            else:
                needsAddList.append(False)                    

        if hasattr(filesPathVoidIn, "__iter__"):
            return needsAddList
        else:
            return needsAddList[0]

    def getChangelists(self,
                        isPendingIn=True,
                       userStrIn=None,
                       clientStrIn=None,
                       *argsListIn):
        """
        Get Perforce Changelists using `p4 changes`

        P4 Changes <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_changes.html>

        Args:
            None

        Keyword Args:
            isPendingIn (bool): Only Pending Changelists
            userStrIn (str): Filter By Users Changelists
            clientStrIn (str): Filter By Client Changelists

        Returns:
            (list): Changelists - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> changelistsList = PerforceWrapper().getChangelists()
                >>> for key, value in changelistsList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # If we are running all defaults call the getPendingChangelists function
        if isPendingIn == True and userStrIn == None and clientStrIn == None:
            return self.getPendingChangelists()

        argsList = []

        # Pending
        if isPendingIn == True:
            argsList.extend(["-s", "pending"])

        # User
        if userStrIn == None:
            argsList.extend(["-u", self.p4Obj.user])

        # Client
        if clientStrIn == None:
            argsList.extend(["-c", self.p4Obj.client])

        # Get the changelists
        resultsList = None

        argsList.extend(argsListIn)

        try:
            resultsList = self.run_changes(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj, False)

        return resultsList

    def getChangelistInfo(self,
                           changelistsVoidIn,
                          isShelvedIn=False,
                          *argsListIn):
        """
        Get Changelist Info using `p4 describe`

        P4 Describe <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_describe.html>

        Args:
            changelistsVoidIn (void): (str/list) Changelist Number(s)

        Keyword Args:
            isShelvedIn (bool): Return Shelved Files instead of changelist files

        Returns:
            (list): Changelist Info Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 4

                >>> from general.perforce import PerforceWrapper
                >>> createdChangelistStr = PerforceWrapper().createChangelist("Test Changelist")
                >>> changelistInfoList = PerforceWrapper().getChangelistInfo(createdChangelistStr)
                >>> PerforceWrapper().deleteChangelist(createdChangelistStr)
                >>> for key, value in changelistInfoList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        argsList = []

        if isShelvedIn:
            argsList = ["-S"]

        # Get the changelists
        changelistsList = self._convertToList(changelistsVoidIn)

        argsList.append(changelistsList)
        argsList.extend(argsListIn)

        resultsList = None

        # Run the describe
        try:
            resultsList = self.run_describe(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList


    def getChangelistNumber(self,
                            descriptionStrIn):
        """
        Get a changelist number based on `descriptionStrIn`

        Calls :func:`core.general.perforce.PerforceWrapper.getChangelists`

        Args:
            descriptionStrIn (str): Changelist Description to search for

        Returns:
            (str): Changelist Number, Returns None if changelist Not Found

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 4

                >>> from general.perforce import PerforceWrapper
                >>> createdChangelistStr = PerforceWrapper().createChangelist("Test Changelist")
                >>> changelistNumberStr = PerforceWrapper().getChangelistNumber("Test Changelist")
                >>> PerforceWrapper().deleteChangelist(createdChangelistStr)
                >>> print changelistNumberStr

        """
        # Get the changelists
        changelistsList = self._getChangelists()

        # Lower the description
        descriptionStrIn = descriptionStrIn.lower()

        if changelistsList is not None:
            # Loop through the changelists
            for currentChangelistDict in changelistsList:
                # Check the description
                if descriptionStrIn in currentChangelistDict["desc"].lower():
                    return currentChangelistDict["change"]

        return None


    def deleteShelvedFiles(self,
                           changelistStrIn,
                           filesVoidIn=None,
                           *argsListIn):
        """
        Delete Shelved Files using `p4 shelve`

        Delete shelved files in `changelistStrIn`, only delete `filesVoidIn` if provided

        P4 Shelve <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_shelve.html>

        Args:
            changelistStrIn (str): Changelist to Delete Shelved Files From

        Keyword Args:
            filesVoidIn (void): (list/str) Shelved File(s) To Delete

        Returns:
            (list): Shelve Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 4, 6, 7, 8

                >>> from general.perforce import PerforceWrapper
                >>> createdChangelistStr = PerforceWrapper().createChangelist("Test Changelist")
                >>> PerforceWrapper().checkout("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt", changelistStrIn=createdChangelistStr)
                >>> PerforceWrapper().run_shelve("-c", createdChangelistStr, "//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> deleteShelvedFilesList = PerforceWrapper().deleteShelvedFiles(createdChangelistStr)
                >>> PerforceWrapper().revert("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> PerforceWrapper().deleteChangelist(createdChangelistStr)
                >>> print deleteShelvedFilesList

        """
        # Build the args
        argsList = ["-d"]
        argsList.extend(["-c", changelistStrIn])

        # Add the files
        filesList = self._convertToList(filesVoidIn)

        if len(filesList) > 0:
            argsList.extend(filesList)

        argsList.extend(argsListIn)

        # Delete the shelved files
        resultsList = None

        try:
            resultsList = self.run_shelve(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList


    def deleteEmptyChangelist(self,
                              doDeleteShelevedIn=False):
        """
        Delete all empty changelists. An empty changelist is defined as a changelist with no files
        and no shelved files

        Args:
            None

        Keyword Args:
            doDeleteShelevedIn (bool): Also deletes shelved files of empty changelists

        Returns:
            (list): Deleted Changelists - Note: Returns None if unable to retrieve changelists

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> createdChangelistStr = PerforceWrapper().createChangelist("Test Changelist")
                >>> print createdChangelistStr
                >>> deleteEmptyChangelistList = PerforceWrapper().deleteEmptyChangelist(createdChangelistStr)
                >>> print deleteEmptyChangelistList

        """
        # Empty Changelists
        emptyChangelistsList = []

        # Get the changelists
        changelistsList = self.getChangelists()

        if changelistsList is None:
            logging.error("Unable to Retrieve Changelists")
            return None

        # Get the changelist numbers
        changelistNumbersList = []

        for changelistDict in changelistsList:
            changelistNumbersList.append(changelistDict["change"])

        # Get the changelist info
        changelistInfoList = self.getChangelistInfo(changelistNumbersList)

        if changelistInfoList is None:
            return emptyChangelistsList

        # Get list of changelists with no files
        for changelistInfoDict in changelistInfoList:
            if "depotFile" not in changelistInfoDict:
                emptyChangelistsList.append(changelistInfoDict["change"])

        # No Empty Changelists
        if len(emptyChangelistsList) == 0:
            return emptyChangelistsList

        # Check for shelved files if `doDeleteShelevedIn`
        changelistInfoList = self.getChangelistInfo(changelistNumbersList, isShelvedIn=True)

        if changelistInfoList is None:
            return emptyChangelistsList

        # Look for empty changelists
        for changelistInfoDict in changelistInfoList:
            if "depotFile" in changelistInfoDict:
                # Delete shelved files of this changelist
                if doDeleteShelevedIn:
                    shelvedChangelistInfoList = self.getChangelistInfo(changelistInfoDict["change"])

                    if "depotFile" not in shelvedChangelistInfoList[0]:
                        logging.info("[PerforceWrapper] Deleting Shelved Files from Changelist: {0}".format(changelistInfoDict["change"]))

                        # Delete the shelved files
                        resultsList = self.deleteShelvedFiles(changelistInfoDict["change"])

                        logging.info("[PerforceWrapper] {0}".format(resultsList))

                # Remove changelist from list of empty changelists
                else:
                    if changelistInfoDict["change"] in emptyChangelistsList:
                        emptyChangelistsList.remove(changelistInfoDict["change"])

        for emptyChangelistStr in emptyChangelistsList:
            resultsList = self.deleteChangelist(emptyChangelistStr)

            if resultsList is not None:
                logging.info("[PerforceWrapper] Deleted empty changelist: {0}".format(emptyChangelistStr))
            else:
                logging.info("[PerforceWrapper] Unable to delete empty changelist: {0}".format(emptyChangelistStr))

        return emptyChangelistsList

    def deleteChangelist(self,
                          changelistVoidIn,
                         *argsListIn):
        """
        Delete Changelist using `p4 change`

        P4 Change <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_change.html>

        Args:
            changelistVoidIn (void): (str/list) Changelist(s)

        Returns:
            (list): Change Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> createdChangelistStr = PerforceWrapper().createChangelist("Test Changelist")
                >>> deleteChangelistList = PerforceWrapper().deleteChangelist(createdChangelistStr)
                >>> print deleteChangelistList

        """
        # Convert to list
        changelistsList = self._convertToList(changelistVoidIn)

        # Build the args
        argsList = ["-d", changelistsList]
        argsList.extend(argsListIn)

        resultsList = None

        # Delete the changelist
        try:
            resultsList = self.run_change(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList

    def modifyChangelistDescription(self,
                                    changelistStrIn,
                                    descriptionStrIn):
        """
        Change the description for a changelist

        Changes the description of `changelistStrIn` to `descriptionStrIn` using `p4 change`

        P4 Change <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_change.html>

        Args:
            changelistStrIn (str): Changelist Number
            descriptionStrIn (str): New Changelist Description

        Returns:
            (str): Changelist Number - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 4

                >>> from general.perforce import PerforceWrapper
                >>> createdChangelistStr = PerforceWrapper().createChangelist("Test Changelist")
                >>> modifiedChangelistStr = PerforceWrapper().modifyChangelistDescription(createdChangelistStr, "New Description")
                >>> PerforceWrapper().deleteChangelist(createdChangelistStr)
                >>> print modifiedChangelistStr

        """
        # Get the changelist
        changelistDict = None

        try:
            changelistDict = self.fetch_change(changelistStrIn)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        # Update the description
        if changelistDict is not None:
            changelistDict["Description"] = descriptionStrIn
        else:
            return None

        # Save the change
        changelistList = None
        try:
            changelistList = self.save_change(changelistDict)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        # Get the changelist number
        if changelistList is not None and len(changelistList) > 0:
            changelistSplitList = changelistList[0].split(" ")

            if len(changelistSplitList) > 1:
                return changelistSplitList[1]

        return None

    def moveFilesToChangelist(self,
                            changelistStrIn,
                              filesVoidIn,
                              *argsListIn):
        """
        Move files to a changelist

        Moved checked out files `filesVoidIn` to `changelistStrIn` using `p4 reopen`

        P4 Reopen <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_reopen.html>

        Args:
            changelistStrIn (str): Changelist to move files to
            filesVoidIn (void): (str/list) File(s) to Move

        Returns:
            (list): Reopen Results - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 5

                >>> from general.perforce import PerforceWrapper
                >>> createdChangelistStr = PerforceWrapper().createChangelist("Test Changelist")
                >>> PerforceWrapper().edit("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> reopenResultsList = PerforceWrapper().moveFilesToChangelist(createdChangelistStr, "//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> PerforceWrapper().revert("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> PerforceWrapper().deleteChangelist(createdChangelistStr)
                >>> print reopenResultsList

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        resultsList = None

        argsList = ["-c", changelistStrIn]
        argsList.extend(filesList)
        argsList.extend(argsListIn)

        try:
            resultsList = self.run_reopen(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj)

        return resultsList


    def moveFiles(self,
                  filePairsListIn,
                  changelistStrIn=None,
                  descriptionStrIn=None):
        """
        Do a perforce move of files

        Move `filePairsListIn` (Source, Dest) in perforce. Create a changelist if `descriptionStrIn`
        is provided or use an existing changelist if `changelistStrIn` is provided

        Calls :func:`core.general.python.PerforceWrapper.move`

        Args:
            filePairsListIn (list): File Pairs List (Source, Dest) To Move

        Keyword Args:
            changelistStrIn (str): Changelist to Move In To
            descriptionStrIn (str): Description of New Changelist to Create

        Returns:
            (str): Changelist - Note: Returns None if Exception Encountered

        Raises:
            (Exception): Raised if invalid move pairs are provided

        Examples:
            To move ``c:\\fileOne.txt`` to ``c:\\fileTwo.txt`` ::

                PerforceWrapper().moveFiles([["C:\\fileOne.txt", "C:\\fileTwo.txt"]])


            .. runblock:: pycon
                :hidden-statements: 1, 3

                >>> from general.perforce import PerforceWrapper
                >>> moveChangelistStr = PerforceWrapper().moveFiles([["//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt", "//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_2.txt"]], descriptionStrIn="Test Changelist")
                >>> PerforceWrapper().deleteChangelist(moveChangelistStr)
                >>> print moveChangelistStr

        """
        # Verify File Pairs
        if isinstance(filePairsListIn, list):
            if len(filePairsListIn) > 0:
                isValidPair = True

                for currentPairList in filePairsListIn:
                    if not isinstance(currentPairList, list):
                        isValidPair = False
                        break

                if not isValidPair:
                    raise Exception("Invalid File Pair List. See documenation for proper use: {0}".format(filePairsListIn))
            else:
                # No Pairs
                return None
        else:
            raise Exception("Invalid File Pair List. See documenation for proper use: {0}".format(filePairsListIn))

        # Determine what changelist to put the move files in to
        changelistStr = None

        if changelistStrIn is None:
            if descriptionStrIn is not None:
                try:
                    changelistStr = self.createChangelist(descriptionStrIn=descriptionStrIn)
                except P4.P4Exception as errorObj:
                    self._logErrors(errorObj)
                    return None
        else:
            changelistStr = changelistStrIn

        if changelistStr is not None:
            # Build the keyword arguments
            keywordArgsDict = {}

            if changelistStrIn is not None:
                keywordArgsDict["changelistStrIn"] = changelistStrIn

            for filePairList in filePairsListIn:
                self.move(*filePairList,
                          **keywordArgsDict)

        return changelistStr


    def deleteFiles(self,
                    filesVoidIn,
                    changelistStrIn=None,
                    descriptionStrIn=None,
                    *argsListIn):
        """
        Delete Files From Perforce

        Deletes `filesVoidIn` from Perforce. Create a changelist if `descriptionStrIn`
        is provided or use an existing changelist if `changelistStrIn` is provided

        Calls :func:`core.general.python.PerforceWrapper.delete`

        Args:
            filesVoidIn (void): (str/list) File(s) to delete

        Keyword Args:
            changelistStrIn (str): Changelist to delete in to
            descriptionStrIn (str): New Changelist Description

        Returns:
            (str): Changelist - Note: Returns None if Exception Encountered

        Examples:

            .. runblock:: pycon
                :hidden-statements: 1, 3, 4

                >>> from general.perforce import PerforceWrapper
                >>> deleteFilesChangelistStr = PerforceWrapper().deleteFiles("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt", descriptionStrIn="Test Changelist")
                >>> PerforceWrapper().revert("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> PerforceWrapper().deleteChangelist(deleteFilesChangelistStr)
                >>> print deleteFilesChangelistStr

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        # Determine what changelist to put the delete files in to
        changelistStr = None

        if changelistStrIn is None:
            if descriptionStrIn is not None:
                try:
                    changelistStr = self.createChangelist(descriptionStrIn=descriptionStrIn)
                except P4.P4Exception as errorObj:
                    self._logErrors(errorObj)
                    return None
        else:
            changelistStr = changelistStrIn

        if changelistStr is not None:
            # Mark the files for delete
            self._delete(filesList,
                         changelistStrIn=changelistStr,
                        *argsListIn)

        return changelistStr

    def checkout(self,
                 filesVoidIn,
                 changelistStrIn=None,
                 descriptionStrIn=None,
                 doOnlyUnchangedIn=False):
        """
        Checkout Files.

        Checkout Files by either opening them for edit or add

        Calls :func:`core.general.python.PerforceWrapper.edit` or
        :func:`core.general.python.PerforceWrapper.add`

        Args:
            filesVoidIn (void): (str/list) File List

        Keyword Args:
            changelistStrIn (str): Changelist to checkout files in to
            descriptionStrIn (str): New Changelist Description
            doOnlyUnchangedIn (bool): Checkout Only Unchanged Files Statuses

        Returns:
            (list): Checkout Results - Note: Returns None if Exception Encountered

        Example:

            .. runblock:: pycon
                :hidden-statements: 1, 3

                >>> from general.perforce import PerforceWrapper
                >>> checkoutResultList = PerforceWrapper().checkout("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> PerforceWrapper().revert("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> for key, value in checkoutResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        # Get the file statuses
        statusDict = self.status([str(file_) for file_ in filesList])

        # Build the add/edit file dictionary
        filesDict = {"add":[], "edit":[]}

        for fileInfoStr in statusDict:
            # Add
            if statusDict[fileInfoStr]["sourceStatus"] == None:
                filesDict["add"].append(fileInfoStr)
            # Already added or checked out by me
            elif statusDict[fileInfoStr]["sourceStatus"]["addedByMe"] or statusDict[fileInfoStr]["sourceStatus"]["checkedOutByMe"]:
                continue
            # Deleted
            elif statusDict[fileInfoStr]["sourceStatus"]["deleted"]:
                filesDict["add"].append(fileInfoStr)
            # Check for unchanged
            else:
                if doOnlyUnchangedIn:
                    diffResultsList = self._diff(fileInfoStr,
                                                 "-f",
                                                "-sa",
                                                "-t")

                    # Edit
                    if diffResultsList == None or len(diffResultsList) > 0:
                        filesDict["edit"].append(fileInfoStr)
                else:
                    filesDict["edit"].append(fileInfoStr)

        # Changelist
        changelistStr = changelistStrIn

        # If both args provided, update description for that changelist
        if changelistStrIn is not None and descriptionStrIn is not None:
            self._modifyChangelistDescription(changelistStrIn,
                                              descriptionStrIn)
        elif descriptionStrIn is not None:
            try:
                # Create the changelist
                changelistStr = self.createChangelist(descriptionStrIn,
                                                       doReuseExistingIn=True)
            except P4.P4Exception as errorObj:
                logging.error("[Perforce Checkout]: Error creating changelist: {0}".format(errorObj))
                return None

        # Results
        resultsList = []

        # Open files for edit
        if filesDict["edit"]:
            editResultsList = self.edit(filesDict["edit"],
                                         changelistStr)

            if editResultsList is not None:
                resultsList.extend(editResultsList)

        # Open files for add
        if filesDict["add"]:
            addResultsList = self.add(filesDict["add"],
                                       changelistStr)

            if addResultsList is not None:
                resultsList.extend(addResultsList)

        ## Get the status dictionary
        #statusDict = self.status(filesList)

        # Force all files that are open for edit/add to be writeable
        for filePathStr, statusDict in statusDict.items():
            if statusDict["sourceStatus"] is not None:
                # Checked out by me or added by me
                if statusDict["sourceStatus"]["checkedOutByMe"] or statusDict["sourceStatus"]["addedByMe"]:
                    # Make sure the file exists
                    if os.path.exists(filePathStr):
                        # Get the file attribute
                        fileAttributesInt = os.stat(filePathStr)[0]

                        if not fileAttributesInt & stat.S_IWRITE:
                            os.chmod(filePathStr,
                                     stat.S_IWRITE)

        # Check results
        if len(resultsList) == 0:
            return None

        return resultsList


    def listUnopenedFiles(self,
                          filesVoidIn):
        """
        List Unopened Files

        Calls :func:`core.general.python.PerforceWrapper.status`

        Args:
            filesVoidIn (void): (list/str) Files

        Returns:
            (list): Unopened Files

        Example:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> unopenedFilesList = PerforceWrapper().listUnopenedFiles("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> print unopenedFilesList

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        # Unopened Files
        unopenedFilesList = []

        # Get the file statuses
        fileStatusesDict = self.status(filesList)

        # Go through the files
        for filePathStr in filesList:
            if (fileStatusesDict[filePathStr]["sourceStatus"] == None
                or not (fileStatusesDict[filePathStr]["sourceStatus"]["checkedOutByMe"] or fileStatusesDict[filePathStr]["sourceStatus"]["addedByMe"])):

                unopenedFilesList.append(filePathStr)

        return unopenedFilesList


    def checkin(self,
                filesVoidIn=None,
                changelistStrIn=None,
                descriptionStrIn=None,
                submitOptionStrIn=None,
                doRaiseErrorsIn=False,
                *argsListIn):
        """
        Check Files In using `p4 submit`

        P4 Submit <http://www.perforce.com/perforce/doc.current/manuals/cmdref/p4_submit.html>

        Args:
            None

        Keyword Args:
            filesVoidIn (void): (str/list) Files to checkin
            changelistStrIn (str): Changelist
            descriptionStrIn (str): Changelist Description
            submitOptionStrIn (str): Submit Option
            doRaiseErrorsIn (bool): Raise Errors

        Notes:
            Unless a changelist is provided, this will create a changelist and move the files into it

        Returns:
            (list): Checkin Results - Note: Returns None if Exception Encountered

        Example:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> PerforceWrapper().checkout("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> checkinResultList = PerforceWrapper().checkin("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt", submitOptionStrIn="submitunchanged")
                >>> for key, value in checkinResultList[0].items():
                >>>     print "{0}:{1}".format(key, value)

        """
        # Submit options used to control Perforce behavior for file submission
        submitOptionsList = [
            # All open files (with or without changes) are submitted to the depot
            # This is the default behavior of Perforce
            "submitunchanged",

            # All open files (with or without changes) are submitted to the depot,
            # and all files are automatically reopened in the default changelist.
            "submitunchanged+reopen",

            # Only those files with content or type changes are submitted to the dpeot.
            # Unchanged files are reverted
            "revertunchanged",

            # Only those files with content or type changes are submitted to the depot and
            # reopened in the default changelist. Unchanged files are reverted and not reopned in the default changelist
            "revertunchanged+reopen",

            # Only those files with content or type changes are submitted to the depot. Any unchagned files are moved to the default changelist.
            "leaveunchanged",

            # Only those files with content or type changes are submitted to the depot. Unchanged files are moved to the
            # default changelist, and changed files are reopened in the default changelist. This option is similar to
            # submitunchanged+reopen, except that no unchagned files are submitted to the depot.
            "leaveunchanged+reopened"
        ]

        # Arguments
        argsList = []

        # Set submit option
        if submitOptionStrIn is not None:
            if submitOptionStrIn in submitOptionsList:
                argsList.extend(["-f", submitOptionStrIn])
            else:
                logging.error("[Perforce Checkin] Error - {0} is an invalid option. Valid submit options: {1}".format(submitOptionStrIn, submitOptionsList))
                return None

        # Create/Modify Changelist
        changelistStr = self._generateChangelist(changelistStrIn, descriptionStrIn)

        # Create changelist for files
        if filesVoidIn is not None:
            # Convert to list
            filesList = self._convertToList(filesVoidIn)

            # Move files to the changelist
            try:
                self._moveFilesToChangelist(changelistStr, filesList)
            except P4.P4Exception as errorObj:
                logging.error("[Perforce moveFilesToChangelist] Error moving files to changelist: {0}".format(errorObj))
                return None

        if changelistStr is not None:
            argsList.extend(["-c", changelistStr])
        else:
            return None

        # Run submit
        resultsList = None

        argsList.extend(argsListIn)

        try:
            resultsList = self.run_submit(*argsList)
        except P4.P4Exception as errorObj:
            self._logErrors(errorObj,
                            doRaiseExceptionIn=doRaiseErrorsIn)

        # Handle if nothing was submitted (e.g. all files reverted unchanged)
        if resultsList is None:
            changelistInfoList = self.getChangelistInfo(changelistStr)

            if changelistInfoList is not None:
                if not "depotFile" in changelistInfoList[0]:
                    logging.warning("[PerforceCheckin] - No files were submitted")
                    self.deleteChangelist(changelistStr)

        return resultsList


    def checkedOutByOthersStatus(self,
                                 filesVoidIn):
        """
        Determine if `filesVoidIn` are checked out by others

        Calls :func:`core.general.python.PerforceWrapper.status`

        Args:
            filesVoidIn (void): (list/str): File(s) to check

        Returns:
            (list): Files checked out by others

        Example:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> checkedOutByOthersStatus = PerforceWrapper().checkedOutByOthersStatus("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> print checkedOutByOthersStatus

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        # Get the statues
        fileStatusesDict = self.status(filesList)

        # Check for other checkouts on requested files. If we find them, abort
        otherEditList = []

        for fileNameStr in filesList:
            sourceStatusDict = fileStatusesDict[fileNameStr]["sourceStatus"]

            if sourceStatusDict is not None:
                if len(sourceStatusDict["otherCheckOut"]) > 0:
                    otherEditList.append("{0} - {1}".format(os.path.splitext(os.path.basename(fileNameStr))[0],
                                                            sourceStatusDict["otherCheckOut"][0]))

        return otherEditList


    def setClient(self,
                  clientStrIn):
        """
        Set the Client to `clientStrIn`

        Args:
            clientStrIn (str): Client Name

        Returns:
            None
        """ 
        return self._setClient(clientStrIn)


    def _setClient(self,
                   clientStrIn):
        """
        Set the Client to `clientStrIn`

        Args:
            clientStrIn (str): Client Name

        Returns:
            None
        """
        if clientStrIn is not None:
            self.p4Obj.client = clientStrIn
            self.clientStr = clientStrIn


    def getLocalPaths(self,
                      filesVoidIn):
        """
        Get the local paths for `filesVoidIn`

        Calls :func:`core.general.python.PerforceWrapper.where`

        Args:
            filesVoidIn (void): (list/str): File(s) to retrieve local paths for

        Returns:
            (list): List of local paths for `filesVoidIn`

        Example:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> localPathList = PerforceWrapper().getLocalPaths("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> print localPathList

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        # Local Paths
        localPathsList = []

        # Run the where
        resultsList = self.where(filesList)

        localPathsList = []

        for currentPathDict in resultsList:
            if currentPathDict is not None and isinstance(currentPathDict, dict):
                localPathsList.append(filepath.FilePath(currentPathDict["path"]))

        # Return
        return localPathsList


    def getDepotPaths(self,
                      filesVoidIn):
        """
        Get the depoth path for `filesVoidIn`

        Calls :func:`core.general.python.PerforceWrapper.where`

        Args:
            filesVoidIn (void): (list/str): File(s) to retrieve depot paths for

        Returns:
            (list): List of depot paths for `filesVoidIn`

        Example:

            .. runblock:: pycon
                :hidden-statements: 1

                >>> from general.perforce import PerforceWrapper
                >>> localPathList = PerforceWrapper().getDepotPaths("//depot/tools/art/python/UnitTests/unitTestModules/Core/data/test_perforce/test_data_1.txt")
                >>> print localPathList

        """
        # Convert to a list
        filesList = self._convertToList(filesVoidIn)

        # Depot Paths
        depotPathsList = []

        # Run the where
        resultsList = self.where(filesList)

        if resultsList is not None:
            # Get the local Paths
            depotPathsList = [filepath.FilePath(pathDict["depotFile"]) for pathDict in resultsList]

        # Return
        return depotPathsList
    
    def _checkStatusBit(self, status, bit):
        return True if (status & bit) else False

    def smartCheckin(self, filePathList, changelistName=None):
        """
        Wrapper function for checking in files

        Args:
            changelistNameStr (list(str), list(Path))

        Returns:
            None
        """
        # If the changlist exist find the changelist number
        if changelistName:
            changelistNumber = self.getChangelistNumber(changelistName)
        else:
            changelistNumber = None

        # If files are exist for sibmit
        if filePathList:
            self.add(filePathList, changelistNumber)

            if filePathList:
                self.checkin(filePathList,
                             changelistStrIn=changelistNumber,
                             descriptionStrIn=changelistName,
                             submitOptionStrIn='revertunchanged')

        # Else remove empty changelist
        else:
            self.deleteEmptyChangelist()

    def smartCheckout(self,
                      filePathsIn,
                      changelistStrIn=None,
                      descriptionStrIn=None,
                      doOnlyUnchangedIn=False,
                      autoSyncIn=True,
                      checkOutEvenByOthersIn=False,
                      checkLoginIn=False):
        """
        Wrapper function for checking out files

        Args:
            filePathsIn (list(str)) : filePathsIn can either be a list of file path str or a single file path str
            changelistStrIn (str)
            descriptionStrIn (str)
            doOnlyUnchangedIn (bool)
            autoSyncIn (bool)
            checkOutEvenByOthersIn (bool): try to check out the file even if there are someone else has it checked out.
            checkLogIn (bool) : check if user is logged in, if not ask user to log in.

        Results:
            1 = file exists in perforce
            3 = file exists and is up to date
            35 = checked out by another user

        Returns:
            None
        """
        filesCheckedOut = []
        filesToSync     = []
        filesOwnByOther = []

        if type(filePathsIn) not in (list, tuple):
            filePathsIn = [filePathsIn]

        # if file is in sync
        for filePath in filePathsIn:

            try:
                fileStatus = self.quickStatus(filePath)[filePath]
            except:
                return self.add([filePath])

            if self._checkStatusBit(fileStatus, STATUS_EXISTS):

                # if the file is already marked for add
                if self._checkStatusBit(fileStatus, STATUS_ADDED):
                    #This is excessive, but it'll make the rest of the logic work for now
                    filesCheckedOut.append(filePath)

                # if the file is owned by another user
                elif self._checkStatusBit(fileStatus, STATUS_CHECKED_OUT_OTHER):
                    fileInfo = self.status(filePath)[filePath]
                    currentOwner = fileInfo['sourceStatus']['otherCheckOut'][0]
                    filesOwnByOther.append({filePath: '\n checked out by {0}'.format(currentOwner)})
                    if checkOutEvenByOthersIn:
                        filesCheckedOut.append(filePath)

                # if files needs to be synced
                elif not self._checkStatusBit(fileStatus, STATUS_UP_TO_DATE):
                    if autoSyncIn:
                        filesToSync.append(filePath)
                        filesCheckedOut.append(filePath)
                    else:
                        filesOwnByOther.append({filePath: '\n not synced to Latest.'})

                # all is good checkout
                elif self._checkStatusBit(fileStatus, STATUS_UP_TO_DATE):
                    filesCheckedOut.append(filePath)

            elif self.where(filePath)[0]:
                filesCheckedOut.append(filePath)

            else:
                # if the file is not the workspace cancel
                # keeping in the convention of all perforce
                # actions handle and return lists
                continue

        # proceed to checkout
        if filesToSync:
            self.sync(filesToSync)

        ## Check out the files
        #if filesCheckedOut:
            #self._checkout(filesCheckedOut,
                           #changelistStrIn,
                          #descriptionStrIn,
                          #doOnlyUnchangedIn)

        ## print the list of files and owners
        #if filesOwnByOther:
            #filePathStr = '\n'
            #for files in filesOwnByOther:
                #for key, value in files.items():
                    #filePathStr += key + value

            #messageBox.spawnAlertMessageBox(messageStrIn=filePathStr,
                                            #titleStrIn='Errors',
                                            #parentObjIn=qtutil.getMayaWindow())

        return filesCheckedOut    


class PerforceConnection(threading.Thread):
    """
    Perforce Connection Worker Thread

    Attributes:
        outQueueObj (object): :py:class:`multiprocessing.Queue` object
        inQueueObj (object): :py:class:`multiprocessing.Queue` object

    Args:
        outQueueObjIn (object): :py:class:`multiprocessing.Queue` object
        inQueueObjIn (object): :py:class:`multiprocessing.Queue` object
    """
    def __init__(self,
                 outQueueObjIn,
                 inQueueObjIn):
        # Init base class
        threading.Thread.__init__(self)

        # Set the attributes
        self.outQueueObj = outQueueObjIn
        self.inQueueObj = inQueueObjIn


    def run(self):
        """
        Thread Runner
        """
        # Get the P4 object
        p4Obj = self.inQueueObj.get()

        if isinstance(p4Obj, P4.P4):
            try:
                if p4Obj.connected():
                    # P4Python is not catching the timeout disconnect case from our P4 server proxy.
                    # Even if the module tells us that it is connected, we still try to reconnect.
                    p4Obj.disconnect()
                p4Obj.connect()   
            except P4.P4Exception as errorObj:
                for currentWarningObj in p4Obj.warnings:
                    logging.warning(currentWarningObj)

                for currentErrorObj in p4Obj.errors:
                    logging.error(currentErrorObj)

            # Connect seems to work whether or not the perforce server
            # is available or not. If we run the info command when perforce is
            # down, the timeout clause should catch and we'll get a more
            # accurate state of perforce
            try:
                infoList = p4Obj.run_info()

                # We might still be getting wrong data types here, we need to check before we return
                if isinstance(infoList, list):
                    pass
                elif isinstance(infoList, bool):                
                    raise ValueError("Returned Bool instead of List")

            except P4.P4Exception as errorObj:
                for currentWarningObj in p4Obj.warnings:
                    logging.warning(currentWarningObj)

                for currentErrorObj in p4Obj.errors:
                    logging.error(currentErrorObj)

                p4Obj = None
            except ValueError as errorObj:
                # We don't have a valid connection if run_info is returning a bool
                p4Obj = None

        # Put in the out queue
        self.outQueueObj.put(p4Obj)

        self.inQueueObj.task_done()
        self.outQueueObj.task_done()

        return


######################################
############# FUNCTIONS ##############
######################################
def ConnectToPerforceWithTimeout(p4ObjIn):
    """
    Connect to perforce with a timeout

    Connect to perforce with a timeout of :py:const:`CONNECTION_TIMEOUT`

    Args:
        p4ObjIn (object): :py:class:`P4.P4` Object

    Returns:
        (object): :py:class:`P4.P4` Object

    Raises:
        (Exception): Connection Timeout
    """
    if isinstance(p4ObjIn, P4.P4):
        # Create the queues
        outQueueObj = queue.Queue()
        inQueueObj = queue.Queue()

        # Put the p4 object into the in queue
        inQueueObj.put(p4ObjIn)

        # Start the connection as a process
        workerObj = PerforceConnection(outQueueObj, inQueueObj)
        workerObj.setDaemon(True)
        workerObj.start()

        # Wait for `CONNECTION_TIMEOUT` seconds
        newP4Obj = None
        try:
            newP4Obj = outQueueObj.get(timeout=CONNECTION_TIMEOUT)
        except queue.Empty as errorObj:
            newP4Obj = None

    else:
        return None

    return newP4Obj


######################################
############### MAIN #################
######################################
'''
p4.run_attribute(["-p", "-n", "sourceFile", "-v", str('stupid-p4'), path])
[{'attr': 'sourceFile',
  'depotFile': '//te.wilson_TEWIL-W1_Legacy/Legacy/Dev/Source/game/characters/humans/base/Human_Male_Base.ModelGeom07c',
  'rev': '64',
  'status': 'set'}]
p4.fstat('-Oa', path)
[{'action': 'edit',
  'actionOwner': 'te.wilson',
  'change': 'default',
  'clientFile': 'D:\\projects\\Legacy\\Dev\\Source\\game\\characters\\humans\\base\\Human_Male_Base.ModelGeom07c',
  'depotFile': '//depot/Assets/DEV/Source/game/characters/humans/base/Human_Male_Base.ModelGeom07c',
  'haveRev': '64',
  'headAction': 'edit',
  'headChange': '101714',
  'headModTime': '1565900127',
  'headRev': '64',
  'headTime': '1565900210',
  'headType': 'binary+lm',
  'isMapped': '',
  'openattr-sourceFile': 'stupid-p4',
  'openattrProp-sourceFile': '',
  'type': 'binary+lm',
  'workRev': '64'}]
p4.fstat('-Oa', path)[0]['openattr-sourceFile']
'stupid-p4'
'''