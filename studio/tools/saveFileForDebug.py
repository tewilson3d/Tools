__TOOLNAME__ = 'Save File For Debug'
__TOOLID__   = '1bed3561-7c2a-11e6-9a2e-d4bed9821440'
__TOOLDESC__ = 'Save .'
__TOOLICON__ = 'default.png'

def main():
	import os
	import maya.cmds as cmds
	import filepath	
	import utilities.save as save
	#from sourceControl.perforceQt.PerforceQtWrapper import smartCheckin

	# grab the file
	currentScenePath = filepath.FilePath(cmds.file(q=True, sn=True)).asMayaPath()
	debugFileScenePath = filepath.ArtPath().join(['TechArt',
	                                              'debuggingTestFiles',
	                                              currentScenePath.basename()])).asMayaPath()
	
	# Save
	save.p4save(currentScenePath)
	save.p4save(debugFileScenePath, perforceCheckIn=True)
	
	# Reopen current file
	cmds.file(currentScenePath, o=True, f=True)