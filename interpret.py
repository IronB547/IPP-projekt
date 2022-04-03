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

CONST_FUNC =   [[1],  # DEFVAR
				[2],  # MOVE
				[3],  # ADD
				[1],  # WRITE
				[0],  # CREATEFRAME
            	[0],  # PUSHFRAME
                [0],  # POPFRAME
                [1],  # CALL
                [0],  # RETURN
                [1],  # PUSHS
                [1],  # POPS
                [3],  # SUB
                [3],  # MUL
                [3],  # IDIV
                [3],  # LT
                [3],  # GT
                [3],  # EQ
                [3],  # AND
                [3],  # OR
                [2],  # NOT
                [2],  # INT2CHAR
                [3],  # STRI2INT
                [2],  # READ
                [1],  # WRITE
                [3],  # CONCAT
                [2],  # STRLEN
                [3],  # GETCHAR
                [3],  # SETCHAR
                [2],  # TYPE
                [1],  # LABEL
                [1],  # JUMP
                [3],  # JUMPIFEQ
                [3],  # JUMPIFNEQ
                [1],  # EXIT
                [1],  # DPRINT
                [0],  # BREA
				]
class Frames:
	def __init__(self):
		self.global_frame = []
		self.tmp_frame = None
		self.frame_stack = []
		self.stack = []
	def add_to_frame(self, f_type, var_name):
		if f_type == "GF":
			self.global_frame.append([var_name])

		if f_type == "LF":
			if len(self.frame_stack) == 0:
				print("No LF on frame stack")
				exit(55)

		if f_type == "TF":
			if self.tmp_frame == None:
				print("No TF created")
				exit(55)
	def search_frame(self, f_type, var_name):
		var_counter = 0
		if f_type == "GF":
			for variable in range(len(self.global_frame)):
				#print(self.global_frame[variable][0], var_name)
				if var_name == self.global_frame[variable][0]:
					var_counter += 1
					#print(var_counter)
				if var_counter > 1:
					print("Redeclaration of " + var_name)
					exit(52)
			#if var_counter == 0:
				#print("Variable " + var_name + " doesn't exist.")
				#exit(52)

		#if f_type == "LF":
			#for variable in self.frame_stack:

		#if f_type == "TF":
			#for variable in self.tmp_frame:

	def return_index(self, f_type, var_name):
		if f_type == "GF":
			index = 0
			for variable in range(len(self.global_frame)):
				if var_name == self.global_frame[variable][0]:
					return index
				index += 1

				# if f_type == "LF":
					# for variable in self.frame_stack:

				# if f_type == "TF":
					# for variable in self.tmp_frame:

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

def get_frame(argument_num):
	return instruction.args[argument_num].value.partition("@")[0]

def var_find_index(argument_num):
	if frames.return_index(get_frame(0), instruction.args[argument_num].value) == None:
		print("Non defined variable" + instruction.args[argument_num].value)
		exit(54)
	return frames.return_index(get_frame(0), instruction.args[argument_num].value)

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

#print("ROOT:", root.tag, root.items(), root.get(key=
frames = Frames()
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

	found_func = False
	for func in Functions:
		if instruction.name == func.name:
			found_func = True
			func_check = CONST_FUNC[func.value][0]
			if func_check != len(instruction.args):
				print("Error 32")
				exit(32)
			break
	#print("\n",instruction.name)

	if found_func == False:
		print("Error 32")
		exit(32)

	# I don't know how else I should solve this, so this will be a switch like structure
	if instruction.name == 'DEFVAR':
		if instruction.args[0].type != 'var':
			print("Incorrect type: " + instruction.args[0].type + " var expected.")
			exit(53)

		frames.search_frame(get_frame(0), instruction.args[0].value)
		frames.add_to_frame(get_frame(0), instruction.args[0].value)
		print(frames.global_frame)

	if instruction.name == 'MOVE':
		#print(instruction.args[0].type, instruction.args[1].type)

		in_var_indx = var_find_index(0)
		if instruction.args[1].type != 'var': # check if second argument is variable or not !!!WARNING!!! not checking if variable has data, TODO
			frames.global_frame[in_var_indx].append(instruction.args[1].type)
			frames.global_frame[in_var_indx].append(instruction.args[1].value)
		else:
			from_var_indx = var_find_index(1)

			#check for more data, if data is present rewrite. TODO
			frames.global_frame[in_var_indx].append(frames.global_frame[from_var_indx][1])
			frames.global_frame[in_var_indx].append(frames.global_frame[from_var_indx][2])

		print(frames.global_frame)
		#print("I read move! and index is", frames.return_index(get_frame(0), instruction.args[0].value))

	if instruction.name == 'ADD':
		print("I read add!")

	if instruction.name == 'WRITE':
		print("I read write!")

	if instruction.name == 'JUMP':
		print("I read jump!")

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