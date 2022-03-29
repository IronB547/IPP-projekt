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

#print("ROOT:", root.tag, root.items(), root.get(key='language'))
first_iter = True
for child in root:
	if child.tag != 'instruction':
		print("Error 32")
		exit (32)

	if first_iter == True:
		if int(child.get(key='order')) == 1:
			op_num = int(child.get(key='order'))
		else:
			print("Error 32")
			exit(32)

	if int(op_num) < 1:
		print("Error 32")
		exit(32)

	if op_num != int(child.get(key='order')) - 1 and first_iter == False:
		print("Error 32")
		exit(32)

	op_num = int(child.get(key='order'))
	first_iter = False

	print("CHILD:", child.tag, child.items(), child.get(key='order'), child.get(key='opcode'))
	instruction = Instruction(name=child.get(key='opcode'), number=child.get(key='order'))

	flag_arg1 = False
	flag_arg2 = False
	for arg in child:
		#print("ARG:", arg.tag, arg.items(), arg.get(key='type'), arg.text, "\n")

		if re.match("arg1", arg.tag):


#		print(len(instruction.args))
#
#		if re.match("arg1", arg.tag):
#			instruction.add_argument(arg.get(key='type'), arg.text)
#			flag_arg1 = True
#			print(len(instruction.args))
#			continue
#
#		if flag_arg1 and re.match("arg2", arg.tag):
#			instruction.add_argument(arg.get(key='type'), arg.text)
#			flag_arg2 = True
#			print(len(instruction.args))
#			continue
#
#		if flag_arg1 and flag_arg2 and re.match("arg3", arg.tag):
#			instruction.add_argument(arg.get(key='type'), arg.text)
#		else:
#			print("Error 32")
#			exit(32)


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