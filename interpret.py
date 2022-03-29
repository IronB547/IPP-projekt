import argparse
import re
import xml.etree.ElementTree as ET

class Argument:
	def __init__(self, arg_type, value):
		self.type = arg_type
		self.value = value

class Instruction:
	def __init__(self, name, number):
		self.name = name
		self.number = number
		self.args = []
	def add_argument(self, arg_type, value):
		self.args.append(Argument(arg_type, value))
		# argparse

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

if root.tag != "program" or root.get(key='language') != "IPPcode22":
	print("Error 32")
	exit (32)

print(root.tag, root.items(), root.get(key='language'))
for child in root:
	if child.tag != 'instruction':
		print("Error 32")
		exit (32)

	print(child.tag, child.items(), child.get(key='order'), child.get(key='opcode'))
	instruction = Instruction(name=child.get(key='opcode'), number=child.get(key='order'))


	for arg in child:
		print(arg.tag, arg.items(), arg.get(key='type'), arg.text, "\n")
		instruction.add_argument(arg.get(key='type'), arg.text)
		print(instruction.args)

	print("\n")

#for instruction in root:
#	print(instruction.keys())
#	print(instruction.items())
#checks

#if root.tag != 'program': # nvm, you MUST check for this, it's also correct, root.tag is program
#	# shod
#
#for child in root:
#	if child.tag != 'instruction': # 
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