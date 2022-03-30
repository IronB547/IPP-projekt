import argparse
import re
import xml.etree.ElementTree as ET
from enum import Enum

class Functions(Enum):
	DEFVAR = 0
	MOVE = 1
	ADD = 2
	WRITE = 3
	CREATEFRAME = 4
	PUSHFRAME = 5
	POPFRAME = 6
	CALL = 7
	RETURN = 8
	PUSHS = 9
	POPS = 10
	SUB = 11
	MUL = 12
	IDIV = 13
	LT = 14
	GT = 15
	EQ = 16
	AND = 17
	OR = 18
	NOT = 19
	INT2CHAR = 20
	STRI2INT = 21
	READ = 22
	CONCAT = 24
	STRLEN = 25
	GETCHAR = 26
	SETCHAR = 27
	TYPE = 28
	LABEL = 29
	JUMP = 30
	JUMPIFEQ = 31
	JUMPIFNEQ = 32
	EXIT = 33
	DPRINT = 34
	BREAK = 35

CONST_FUNC = 	[[1, 'DEFVAR'],
				[2, 'MOVE'],
				[3, 'ADD'],
				[1, 'WRITE'],
				[0, 'CREATEFRAME'],
            	[0, 'PUSHFRAME'],
                [0, 'POPFRAME'],
                [1, 'CALL'],
                [0, 'RETURN'],
                [1, 'PUSHS'],
                [1, 'POPS'],
                [3, 'SUB'],
                [3, 'MUL'],
                [3, 'IDIV'],
                [3, 'LT'],
                [3, 'GT'],
                [3, 'EQ'],
                [3, 'AND'],
                [3, 'OR'],
                [2, 'NOT'],
                [2, 'INT2CHAR'],
                [3, 'STRI2INT'],
                [2, 'READ'],
                [1, 'WRITE'],
                [3, 'CONCAT'],
                [2, 'STRLEN'],
                [3, 'GETCHAR'],
                [3, 'SETCHAR'],
                [2, 'TYPE'],
                [1, 'LABEL'],
                [1, 'JUMP'],
                [3, 'JUMPIFEQ'],
                [3, 'JUMPIFNEQ'],
                [1, 'EXIT'],
                [1, 'DPRINT'],
                [0, 'BREAK']
				]

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

	print("CHILD:", child.get(key='order'), child.get(key='opcode'), child.tag, child.items())
	instruction = Instruction(name=child.get(key='opcode'), number=child.get(key='order'))

	flag_arg1 = False
	flag_arg2 = False
	for arg in child:
		#print("ARG:", arg.tag, arg.items(), arg.get(key='type'), arg.text, "\n")

		if re.match("arg1", arg.tag):
			instruction.add_argument(arg.get(key='type'), arg.text)
			flag_arg1 = True

		elif re.match("arg2", arg.tag) and flag_arg1:
			instruction.add_argument(arg.get(key='type'), arg.text)
			flag_arg2 = True

		elif re.match("arg3", arg.tag) and flag_arg2:
			instruction.add_argument(arg.get(key='type'), arg.text)

		elif not flag_arg1:
			print("Error 32")
			exit(32)

	found_func = False
	for func in Functions:
		if instruction.name == func.name:

			found_func = True
			func_check = CONST_FUNC[func.value][0]
			if func_check != len(instruction.args):
				print("Error 32")
				exit(32)

	if found_func == False:
		print("Error 32")
		exit(32)


	# len(instruction.args), instruction.name
	print("FUNCTIONS: read operands:", len(instruction.args), "opcode", instruction.number, "\n")

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