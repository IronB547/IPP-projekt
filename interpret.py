import argparse
import re
import xml.etree.ElementTree as ET
from xml.parsers.expat import ParserCreate, ExpatError, errors

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

parse_check = ParserCreate()

print(args.source[0])

#try:
#	parse_check.Parse(args.source[0])
#except ExpatError as err:
#
#	print(err)
#	print(errors.messages[4])
#	exit (31)
#
#	if err == errors.messages[4]:
#		print(err, "\n")
#		print(errors.messages[4])
#		exit (31)

	#	exit (31)

# load xml
tree = ET.parse(args.source[0])

root = tree.getroot()

print(root.tag, root.attrib)
for child in root:
	print(child.tag, child.attrib)


#checks

#if root.tag != 'program':
#	# shod
#
#for child in root:
#	if child.tag != 'instruction':
#		# shod
#
#	ca = list(child.attrib.keys())
#	if not('order')
#		# shod
#
#	for subelem in child:
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