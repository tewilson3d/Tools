import xml.etree.ElementTree as xml
import xml.dom.minidom as minidom


def writeToXml(filePath, doc, prettyXml=False):
	"""will write the file to XML - prettyXml will lay the code out properly
	it does slow the write down though"""

	#Open a file
	file = open(filePath, 'w')

	xmlStr = ""
	if prettyXml:
		xmlStr = minidom.parseString(xml.tostring(doc)).toprettyxml()
	else:
		xmlStr = xml.tostring(doc)

	#write out everything
	file.write(xmlStr)

	#Close the file like a good programmer
	file.close()

def toBool(boolString):
	"""when parsing an xml file, this will cast the string to a bool"""
	if boolString == "True":
		return True
	elif boolString == "False":
		return False