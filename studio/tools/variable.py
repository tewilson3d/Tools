import os

class Variable(object):
    def __init__(self):
        self._filePath = os.path.dirname(os.path.abspath(__file__))
        self._dept = 'art'
        self._type = 'rig'
        self._app = 'maya'
        self._appVersion = '2018'

        self.toolPath = ''
        self.deptPath = ''
        self.typePath = ''
        self.scriptPath = ''
        self.pluginPath = ''
        self.scenePath = ''
        self.controlPath = ''
        self.templatePath = ''
    
    @property
    def dept(self):
        return self._dept

    @dept.setter
    def dept(self, value):
        self._dept = value
        self.updateVairable()

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, value):
        self._app = value
        self.updateVairable()

    @property
    def appVersion(self):
        return self._appVersion

    @appVersion.setter
    def appVersion(self, value):
        self._appVersion = value
        self.updateVairable()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
        self.updateVairable()
    
    def updateVairable(self):
        self.deptPath = r'{0}\{1}'.format(self._filePath, self._dept)
        self.toolPath = r'{0}\{1}'.format(self.deptPath, 'tool')
        self.typePath = r'{0}\{1}'.format(self.toolPath, self._type)
        self.scriptPath = r'{0}\{1}\{2}\{3}'.format(self.typePath, self._app, self._appVersion, 'scripts')
        self.pluginPath = r'{0}\{1}\{2}\{3}'.format(self.typePath, self._app, self._appVersion, 'plugins')
        self.scenePath = r'{0}\{1}\{2}\{3}'.format(self.typePath, self._app, self._appVersion, 'scenes')
        self.controlPath = r'{0}\{1}'.format(self.scenePath, 'control') + '\\'
        self.templatePath = r'{0}\{1}'.format(self.scenePath, 'template') + '\\'

