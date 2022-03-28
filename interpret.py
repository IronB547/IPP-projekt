import argparse
import re
import xml.etree.ElementTree as ET

class arg:
	def __init__(self, arg_type, value):
		self.type = arg_type
		self.value = value

class instruction:
	def __init__(self, name, number):
		self.name = name
		self.number = number
		self.args = []
	def add_argument(self, arg_type, value):
		self.args.append(arg(arg_type, value))
		# argparse

def listToString(list):
	str1 = " "

	return (str1.join(list))

argp = argparse.ArgumentParser()
argp.add_argument("--source", nargs= 1, type=argparse.FileType('r'), help= "TODO")
argp.add_argument("--input", nargs= 1, help= "TODO")

args = argp.parse_args()

try:
	tree = ET.parse(args.source[0])
except:
	print("Error 31")
	exit (31)

# load xml
root = tree.getroot()
elem = ET.ElementTree(args.source[0])

#print(elem.getroot())
print(root.tag, root.attrib)
for child in root:
	print(child.tag, child.attrib)


#checks

#if root.tag != 'program': # don't have to, already error 31
#	# shod
#
#for child in root:
#	if child.tag != 'instruction': # don't have to, already error 31
#		# shod
#
#	ca = list(child.attrib.keys()) # I need to check these
#	if not('order')
#		# shod
#
#	for subelem in child: # idk much about this but we'll see
#		if not(re.match(r"arg[123]", subelem.tag)):
#			#shod
#
## xml 2 instruction
#for elem in root:
#	#make instruction
#	for sub in elem:
#		instruction.add_argument(arg_type, value)
#
#for i in instructions:
#	interpret(i)