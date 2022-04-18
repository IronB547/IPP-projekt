# Principy programovacích jazyků a OOP (IPP)
# Interpret.py
# Author: Tomáš Dvořák 
# Login: xdvora3r

import argparse
import xml.etree.ElementTree as ET
from enum import Enum
import sys
import re
import os.path
from io import StringIO


# BEGINNING of Functions and Classes
# Enumeration class, I have forgotten about dictionaries, and it was too late for me to change the code, I have made
# many changes/functions before I remembered they existed.
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
	CONCAT = 23
	STRLEN = 24
	GETCHAR = 25
	SETCHAR = 26
	TYPE = 27
	LABEL = 28
	JUMP = 29
	JUMPIFEQ = 30
	JUMPIFNEQ = 31
	EXIT = 32
	DPRINT = 33
	BREAK = 34


# A Constant array of function in IPPcode, as mentioned earlier, a dictionary would fit this purpose better.
CONST_FUNC = 	[[1],  # DEFVAR
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
				[0],  # BREAK
				]


# Class Frames - Implements all frames in a class structure, it's my first time working with them, so
# I hope I haven't made too many mistakes.
# Every frame is implemented via a list, each variable is represented as a list inside said list, so variables in
# frames would look like this: [['frame@var1', 'type', 'value'], ['frame@var2', 'type', 'value']] etc.
# Empty variables do not have 'type', nor 'value', just a name in the list.
# However, local frame is implemented with frame_stack, I am working with a list just like I would with stack, so I
# append/pop the last list accordingly. Variables in local frame would look something like this:
# [[[LF@var1], [LF@var2]], [[LF@VAR1], [LF@VAR2]]]. First list is the frame itself, second list is each individual
# temporary frame and third list is composed of individual variables. The rightmost list is the top of the stack.
# This rule applies to every stack-like structure I have used.
class Frames:
	def __init__(self):
		self.global_frame = []  # Global frame.
		self.tmp_frame = None  # Temporary frame.
		self.frame_stack = []  # Local frame.
		self.stack = []  # Stack for PUSHS and POPS functions.
		self.call_stack = []  # Stack for CALL and RETURN functions.
		self.labels = []  # A list of labels, that is filled in by the first run through of the xml code.

	# add_to_labels method - Inserts labels into label list.
	# A for cycle iterates through the list to find duplicate label names.
	def add_to_labels(self, label_name, index):
		for name in self.labels:
			if label_name == name[0]:
				print("Same label name " + label_name, file=sys.stderr)
				exit(52)
		self.labels.append([label_name, index])

	# search_labels method - Looks and return a label name from the label list.
	def search_labels(self, label_name):
		for name in self.labels:
			if label_name == name[0]:
				return name

	# add_to_frame method - Implements insertion of variables to any frame.
	# Redeclaration of variables is checked via search_frame method, this method simply adds variables.
	# Temporary and local frames are an exception, we cannot add variables to empty frame.
	def add_to_frame(self, f_type, var_name):
		if f_type == "GF":
			self.global_frame.append([var_name])

		if f_type == "LF":
			if len(self.frame_stack) == 0:
				print("No LF on frame stack", file=sys.stderr)
				exit(55)

			self.frame_stack[len(self.frame_stack) - 1].append([var_name])

		if f_type == "TF":
			if self.tmp_frame is None:
				print("No TF created", file=sys.stderr)
				exit(55)

			self.tmp_frame.append([var_name])

	# search_frame method - Checks if variable exists on frame or not.
	# For DEFVAR, no variable must be present, in order to define a new one.
	# For any other function, only one variable must be present, we cannot have multiple variables.
	def search_frame(self, f_type, var_name):
		var_counter = 0
		if f_type == "GF":
			for variable in range(len(self.global_frame)):
				if var_name == self.global_frame[variable][0]:
					var_counter += 1

			if instruction.name == 'DEFVAR' and var_counter > 0:
				print("Redeclaration of variable: " + var_name, file=sys.stderr)
				exit(52)
			elif instruction.name != 'DEFVAR' and var_counter == 0:
				print("Variable " + var_name + " doesn't exist.", file=sys.stderr)
				exit(54)

		elif f_type == "LF":
			if len(self.frame_stack) < 1:
				print("Empty Local frame", file=sys.stderr)
				exit(55)

			for variable in range(len(self.frame_stack)):
				if len(self.frame_stack[LF_len()]) == 0:
					break
				if var_name == self.frame_stack[LF_len()][len(self.frame_stack[LF_len()]) - 1][0]:
					var_counter += 1

			if instruction.name == 'DEFVAR' and var_counter > 0:
				print("Redeclaration of variable: " + var_name, file=sys.stderr)
				exit(52)
			elif instruction.name != 'DEFVAR' and var_counter == 0:
				print("Variable " + var_name + " doesn't exist.", file=sys.stderr)
				exit(54)

		elif f_type == "TF":
			if self.tmp_frame is None:
				print("Temporary Frame has not been created", file=sys.stderr)
				exit(55)

			for variable in range(len(self.tmp_frame)):
				if var_name == self.tmp_frame[variable][0]:
					var_counter += 1

			if instruction.name == 'DEFVAR' and var_counter > 0:
				print("Redeclaration of variable: " + var_name, file=sys.stderr)
				exit(52)
			elif instruction.name != 'DEFVAR' and var_counter == 0:
				print("Variable " + var_name + " doesn't exist.", file=sys.stderr)
				exit(54)

	# return_index method - Finds the index of a variable in any frame.
	# If TF or LF frame is empty, throw exception.
	def return_index(self, f_type, var_name):
		index = 0
		if f_type == "GF":
			for variable in range(len(self.global_frame)):
				if var_name == self.global_frame[variable][0]:
					return index
				index += 1

		elif f_type == "LF":
			if len(self.frame_stack) < 1:
				print("Empty Local frame", file=sys.stderr)
				exit(55)

			for variable in range(len(self.frame_stack[len(self.frame_stack) - 1])):
				if var_name == self.frame_stack[LF_len()][variable][0]:
					return index
				index += 1

		elif f_type == "TF":
			if frames.tmp_frame is None:
				print("Empty Temp frame", file=sys.stderr)
				exit(55)

			for variable in range(len(self.tmp_frame)):
				if var_name == self.tmp_frame[variable][0]:
					return index
				index += 1


# Argument class - Used for storing arguments from xml source file.
# Class is mainly used by Instruction class, which stores all the necessary information about processed instruction.
# arg_type = string, type of argument.
# value = string, value of argument.
class Argument:
	def __init__(self, arg_type, value):
		self.type = arg_type
		self.value = value


# Instruction class - Used for storing data of processed instruction.
# name = name of opcode i.e. DEFVAR, MOVE, JUMP, etc.
# args = list that has a type and value of processed instruction.
class Instruction:
	def __init__(self, name):
		self.name = name
		self.args = []

	# add_argument method - Inserts values inside the args list.
	def add_argument(self, arg_type, value):
		self.args.append(Argument(arg_type, value))


# Function get_frame - Various functions are called by taking the frame of the variable, name of variable and values.
# argument_num = int, which argument is being processed (1,2 or 3).
# For example, if a function requires a frame, such as insert_into_var(), get_frame function return 'GF', 'LF' or 'TF'.
def get_frame(argument_num):
	return instruction.args[argument_num].value.partition("@")[0]


# Function check_type_var - Checks if argument (1,2 or 3) is a variable or not.
def check_type_var(arg_num):
	if instruction.args[arg_num].type == 'var':
		return True
	else:
		return False


# Function LF_len - Returns length of frame stack.
# Used for indexing the last temporary frame inside local frame.
def LF_len():
	return len(frames.frame_stack) - 1


# Function to_LF - Converts temporary frame variables to local frame variables.
# Throw exception, if temporary frame is empty.
def to_LF():
	if frames.tmp_frame is None:
		print("Empty Temp frame", file=sys.stderr)
		exit(55)

	for variable in frames.tmp_frame:
		new_var = variable[0].partition("@")

		new_var = list(new_var)
		new_var[0] = 'LF'
		new_var = "".join(new_var)

		variable[0] = new_var


# Function to_TF - Converts local frame variables to temporary frame variables.
def to_TF():
	for variable in frames.tmp_frame:
		new_var = variable[0].partition("@")
		new_var = list(new_var)
		new_var[0] = 'TF'
		new_var = "".join(new_var)

		variable[0] = new_var


# Function var_find_index - Simplification as well as throwing exception each time we need to find index of a variable.
# argument_num = int, which argument is being processed (1,2 or 3).
# Function returns the index of variable inside any frame.
def var_find_index(argument_num):
	if frames.return_index(get_frame(argument_num), instruction.args[argument_num].value) is None:
		print("Non defined variable " + instruction.args[argument_num].value, file=sys.stderr)
		exit(54)

	return frames.return_index(get_frame(argument_num), instruction.args[argument_num].value)


# Function find_var - Further simplification, after we find the index, we take the entire variable and return it.
# frame = string, on what frame is the variable is located.
# from_var_indx = int, where is the variable located.
# Checks for empty variable for various reasons.
def find_var(frame, from_var_indx):
	if frame == 'GF':
		if len(frames.global_frame[from_var_indx]) > 1:
			return frames.global_frame[from_var_indx]
		else:
			if instruction.name == 'TYPE':
				return None
			else:
				print("Variable " + frames.global_frame[from_var_indx][0] + " is empty.", file=sys.stderr)
				exit(56)

	elif frame == 'LF':
		if len(frames.frame_stack[LF_len()][from_var_indx]) > 1:
			return frames.frame_stack[LF_len()][from_var_indx]
		else:
			if instruction.name == 'TYPE':
				return None
			else:
				print("Variable " + frames.frame_stack[LF_len()][from_var_indx][0] + " is empty.", file=sys.stderr)
				exit(56)

	elif frame == 'TF':
		if len(frames.tmp_frame[from_var_indx]) > 1:
			return frames.tmp_frame[from_var_indx]
		else:
			if instruction.name == 'TYPE':
				return None
			else:
				print("Variable " + frames.tmp_frame[from_var_indx][0] + " is empty.", file=sys.stderr)
				exit(56)

# Function convert_ascii - Function correctly converts escape sequences into ascii values.
# val = string, value to be converted.
# Returns converted string with correct escaped sequences.
def convert_ascii(val):
	if val is not None:
		index = 0
		for char in val:
			if char == "\\":
				convert = val[index + 1:index + 4]
				try:
					chr(int(convert))
				except ValueError:
					break
				val = val.replace(val[index:index + 4], chr(int(convert)))
				index -= 3
			index += 1

	return val

# Function insert_into_var - Very important function, inserts into correct variable in any frame.
# frame = string, on what frame is the variable is located.
# to_var_indx = int, where the number is located (in frame).
# from_type = string, 'type' of value to be inserted.
# from_value = string, 'value' of value to be inserted.
# Function correctly appends new values, or changes already set values.
def insert_into_var(frame, to_var_indx, from_type, from_value):
	if frame == 'GF':
		from_value = convert_ascii(from_value)
		if len(frames.global_frame[to_var_indx]) > 1:
			frames.global_frame[to_var_indx][1] = from_type
			frames.global_frame[to_var_indx][2] = from_value
		else:
			frames.global_frame[to_var_indx].append(from_type)
			frames.global_frame[to_var_indx].append(from_value)

	elif frame == 'LF':
		from_value = convert_ascii(from_value)
		if len(frames.frame_stack[len(frames.frame_stack) - 1][to_var_indx]) > 1:
			frames.frame_stack[LF_len()][to_var_indx][1] = from_type
			frames.frame_stack[LF_len()][to_var_indx][2] = from_value
		else:
			frames.frame_stack[LF_len()][to_var_indx].append(from_type)
			frames.frame_stack[LF_len()][to_var_indx].append(from_value)
	elif frame == 'TF':
		from_value = convert_ascii(from_value)
		if len(frames.tmp_frame[to_var_indx]) > 1:
			frames.tmp_frame[to_var_indx][1] = from_type
			frames.tmp_frame[to_var_indx][2] = from_value
		else:
			frames.tmp_frame[to_var_indx].append(from_type)
			frames.tmp_frame[to_var_indx].append(from_value)


# Function arithm_oper - Simple function used to not repeat code for ADD, SUB, MUL, IDIV functions.
# arg_num = int, which argument is being processed (1,2 or 3).
# from_var_indx = int, where is the variable located.
# Checks for correct type of value and returns it.
def arithm_oper(arg_num, from_var_indx):
	val = find_var(get_frame(arg_num), from_var_indx)
	if val[1] == 'int':
		val = val[2]
	else:
		print("Incorrect type " + val[1], file=sys.stderr)
		exit(53)

	return val


# Function logic_oper - Same as arithm_oper, but just for AND, OR, NOT.
# arg_num = int, which argument is being processed (1,2 or 3).
# from_var_indx = int, where is the variable located.
# Checks for correct type of value and returns it.
def logic_oper(arg_num, from_var_indx):
	val = find_var(get_frame(arg_num), from_var_indx)
	if val[1] == 'bool':
		val = val[2]
	else:
		print("Incorrect type " + instruction.args[arg_num].type, file=sys.stderr)
		exit(53)

	return val


# Function get_val - Simplification of getting values from arguments.
# arg_num = int, which argument is being processed (1,2 or 3).
# Type 'string' with None value is interpreted as empty string.
# Returns the value of argument, if variable, get variable value.
def get_val(arg_num):

	if check_type_var(arg_num):
		from_var_indx = var_find_index(arg_num)
		val = find_var(get_frame(arg_num), from_var_indx)
		val = val[2]
	else:
		if instruction.args[arg_num].type == 'string' and instruction.args[arg_num].value is None:
			return ''

		val = instruction.args[arg_num].value
		val = convert_ascii(val)

	return val


# Function get_type - Simplification of getting types from arguments.
# arg_num = int, which argument is being processed (1,2 or 3).
# Type 'string' with None value is interpreted as empty string.
# Returns the type of argument, if variable, get variable type.
def get_type(arg_num):
	if check_type_var(arg_num):
		from_var_indx = var_find_index(arg_num)
		val_type = find_var(get_frame(arg_num), from_var_indx)
		val_type = val_type[1]
	else:
		val_type = instruction.args[arg_num].type

	return val_type


# Function check_same_type - Used to determine if function has same types.
# type1 = string, type of first argument/variable.
# type2 = string, type of second argument/variable.
# Function returns the matched type, otherwise throws exception
def check_same_type(type1, type2):
	if type1 == 'int' and type2 == 'int':
		return 'int'
	elif type1 == 'bool' and type2 == 'bool':
		return 'bool'
	elif type1 == 'string' and type2 == 'string':
		return 'string'
	elif type1 == 'nil' and type2 == 'nil':
		return 'nil'
	else:
		print("Not same types", file=sys.stderr)
		exit(53)
# END of Functions and Classes


# BEGINNING of Interpreter
# Now begins the actual code. First, we need to parse arguments like --source and --input. For that, I chose argparse.
# It was the easiest to understand and implement.
argp = argparse.ArgumentParser()
argp.add_argument("--source", nargs=1, type=argparse.FileType('r'), help="Path to the '.src' file, can also be loaded from STDIN. Only one source may be read from STDIN")
argp.add_argument("--input", nargs=1, help="Path to the '.in' file. Only one source may be read from STDIN" )

args = argp.parse_args()

# Load files inside variables
source_file = args.source
input_file = args.input

# Here we check if file exists, as well as correct usage of both parameters.
if args.source is not None and args.input is not None:
	if os.path.exists(args.input[0]):
		input_file = args.input[0]
	else:
		print("Cannot open file " + args.input[0], file=sys.stderr)
		exit(11)

	if os.path.exists(args.source[0].name):
		source_file = args.source
	else:
		print("Cannot open file " + args.source[0], file=sys.stderr)
		exit(11)
elif args.source is not None and args.input is None:
	if os.path.exists(args.source[0].name):
		source_file = args.source
	else:
		print("Cannot open file " + args.source[0], file=sys.stderr)
		exit(11)

elif args.source is None and args.input is not None:
	if os.path.exists(args.input[0]):
		input_file = args.input[0]
	else:
		print("Cannot open file " + args.input[0], file=sys.stderr)
		exit(11)

	source_file = []
	source_file.append(False)
else:
	print("Incorrect combination of input files, use --h, --help for more info", file=sys.stderr)
	exit(10)

# Now, onto parsing the XML file. I have used the Etree library.
# Try EtreeParse, if parse error, throw exception.
try:
	tree = ET.parse(source_file[0])
except ET.ParseError:
	print("File is not well formed", file=sys.stderr)
	exit(31)
else:
	pass

# Get root of the tree.
root = tree.getroot()

# Now come a lot of XML structure checks.
# Incorrect program language.
if root.tag != "program" or root.get(key='language') != "IPPcode22":
	print("Incorrect language", file=sys.stderr)
	exit(32)

frames = Frames()
first_iter = True

# Firstly, I iterate through the entire file, check XML structure of instructions,
# sort operands by numbers for the second run through.
for child in root:
	try:
		root[:] = sorted(root, key=lambda child: int(child.get(key='order')))
	except TypeError:
		print("Incorrect element", file=sys.stderr)
		exit(32)
	except ValueError:
		print("Incorrect order type", file=sys.stderr)
		exit(32)
	else:
		root[:] = sorted(root, key=lambda child: int(child.get(key='order')))

# Second run through.
# Sorting arguments by numbers, checking correct XML structure of each argument.
op_num = 0
index = 0
for child in root:
	try:
		child.items()[1]
	except IndexError:
		print("Missing order", file=sys.stderr)
		exit(32)

	edit = child.get(key='opcode')
	edit = edit.upper()
	child.set('opcode', edit)

	if child.tag != 'instruction':
		print("Child has wrong tag", file=sys.stderr)
		exit(32)

	found_func = False
	for func in Functions:
		if child.get(key='opcode') == func.name:
			found_func = True
			func_check = CONST_FUNC[func.value][0]
			if func_check != len(child):
				print("Invalid amount of arguments", file=sys.stderr)
				exit(32)
			break

	for argument in child:
		if not re.match('^arg[1-3]$', argument.tag):
			print("Argument has wrong tag", file=sys.stderr)
			exit(32)
		if op_num >= int(child.get(key='order')):
			print("Incorrect order number", file=sys.stderr)
			exit(32)

		if found_func is False:
			print("Incorrect OPCODE name " + child.get(key='opcode'))
			exit(32)

		child[:] = sorted(child, key=lambda argument: argument.tag)

	op_num = int(child.get(key='order'))
	arg1_flag = False
	arg2_flag = False
	for argument in child:

		if argument.tag == 'arg1' and arg1_flag is False and arg2_flag is False:
			arg1_flag = True
		elif argument.tag == 'arg2' and arg1_flag is True and arg2_flag is False:
			arg2_flag = True
		elif argument.tag == 'arg3' and arg1_flag is True and arg2_flag is True:
			continue
		else:
			print("Missing arguments", file=sys.stderr)
			exit(32)

		if child.get(key='opcode') == 'LABEL':
			frames.add_to_labels(argument.text, index)

	try:
		int(child.get(key='order'))
	except ValueError:
		print("File is not well formed", file=sys.stderr)
		exit(32)

	index += 1


# Third and final run through. Actual interpreting of the XML file.
i = 0
line_count = 0
child = list(root)

# I have selected while for easy jumps.
# Iterate through root (program in XML).
while i < len(root):

	# Load instruction
	instruction = Instruction(name=child[i].get(key='opcode'))

	# Iterate through each child (instruction in XML).
	for arg in child[i]:
		instruction.add_argument(arg.get(key='type'), arg.text)  # Get type and value in class Instruction.

	# Again, I paid here for not using the dictionary, but it was too late. Switch like structure.
	# Sadly, run time is going to be slow, it already is going to be with big frames and loops.
	if instruction.name == 'DEFVAR':
		if instruction.args[0].type != 'var':
			print("Incorrect type: " + instruction.args[0].type + " var expected.", file=sys.stderr)
			exit(53)

		frames.search_frame(get_frame(0), instruction.args[0].value)
		frames.add_to_frame(get_frame(0), instruction.args[0].value)

	elif instruction.name == 'MOVE':
		frames.search_frame(get_frame(0), instruction.args[0].value)

		to_var_indx = var_find_index(0)
		if instruction.args[1].type != 'var':  # check if second argument is variable or not
			insert_into_var(get_frame(0), to_var_indx, instruction.args[1].type, instruction.args[1].value)
		else:
			frames.search_frame(get_frame(1), instruction.args[1].value)
			from_var_indx = var_find_index(1)
			val_type = find_var(get_frame(1), from_var_indx)
			value = find_var(get_frame(1), from_var_indx)

			insert_into_var(get_frame(0), to_var_indx, val_type[1], value[2])

	elif instruction.name == 'READ':
		to_var_indx = var_find_index(0)

		if input_file is None:
			try:
				inp = input()
			except EOFError:
				insert_into_var(get_frame(0), to_var_indx, 'nil', 'nil')
				i += 1
				continue
			else:
				pass

		else:
			file = open(input_file, 'r')
			inp = file.read()
			inp = inp.splitlines()
			try:
				inp[line_count]
			except IndexError:
				insert_into_var(get_frame(0), to_var_indx, 'nil', 'nil')
				i += 1
				continue
			else:
				inp = inp[line_count]

		val_type = get_val(1)

		if val_type == 'int':
			try:
				int(inp)
			except ValueError:
				input_type = 'nil'
			else:
				input_type = 'int'
		else:
			if val_type == 'bool':
				input_type = 'bool'
			else:
				if val_type == 'string':
					input_type = 'string'
				else:
					input_type = 'nil'

		if val_type == 'bool':
			if inp.lower() == 'true':
				insert_into_var(get_frame(0), to_var_indx, val_type, 'true')
			else:
				insert_into_var(get_frame(0), to_var_indx, val_type, 'false')
		elif val_type == 'nil':
			insert_into_var(get_frame(0), to_var_indx, val_type, 'nil')
		else:
			insert_into_var(get_frame(0), to_var_indx, input_type, inp)

		if input_file is not None:
			file.close()

		line_count += 1

	elif instruction.name == 'WRITE':
		val = get_val(0)

		if get_type(0) == 'nil':
			val = ''
		print(val, end='')

	elif instruction.name == 'JUMP':
		label = frames.search_labels(instruction.args[0].value)

		if label is not None:
			i = int(label[1])
		elif label is None:
			print("No label " + instruction.args[0].value + " found", file=sys.stderr)
			exit(52)

	elif instruction.name == 'JUMPIFEQ':
		label = frames.search_labels(instruction.args[0].value)

		val1 = get_val(1)
		val2 = get_val(2)

		type1 = get_type(1)
		type2 = get_type(2)

		check_type = False
		if type1 == 'int' and type2 == 'int':
			check_type = True
		elif type1 == 'bool' and type2 == 'bool':
			check_type = True
		elif type1 == 'string' and type2 == 'string':
			if val1 is None:
				val1 = ''
			if val2 is None:
				val2 = ''
			check_type = True

		elif type1 == 'nil' or type2 == 'nil':
			check_type = True

		if label is not None and val1 == val2:
			i = int(label[1])
		elif label is None:
			print("No label " + instruction.args[0].value + " found", file=sys.stderr)
			exit(52)

		if check_type is False:
			print("Incorrect type", file=sys.stderr)
			exit(53)

	elif instruction.name == 'JUMPIFNEQ':
		label = frames.search_labels(instruction.args[0].value)

		val1 = get_val(1)
		val2 = get_val(2)

		type1 = get_type(1)
		type2 = get_type(2)

		check_type = False
		if type1 == 'int' and type2 == 'int':
			check_type = True
		elif type1 == 'bool' and type2 == 'bool':
			check_type = True
		elif type1 == 'string' and type2 == 'string':
			if val1 is None:
				val1 = ''
			if val2 is None:
				val2 = ''
			check_type = True

		elif type1 == 'nil' or type2 == 'nil':
			check_type = True

		if label is not None and val1 != val2:
			i = int(label[1])
		elif label is None:
			print("No label " + instruction.args[0].value + " found", file=sys.stderr)
			exit(52)

		if check_type is False:
			print("Incorrect type", file=sys.stderr)
			exit(53)

	elif instruction.name == 'CALL':
		label = frames.search_labels(instruction.args[0].value)
		frames.call_stack.append(i)
		if label is not None:
			i = int(label[1])
		elif label is None:
			print("No label " + instruction.args[0].value + " found", file=sys.stderr)
			exit(52)

	elif instruction.name == 'RETURN':
		if len(frames.call_stack) < 1:
			print("Callstack is empty", file=sys.stderr)
			exit(56)
		else:
			i = frames.call_stack[len(frames.call_stack) - 1]
			del frames.call_stack[len(frames.call_stack) - 1]

	elif instruction.name == 'CREATEFRAME':
		frames.tmp_frame = []

	elif instruction.name == 'PUSHFRAME':

		to_LF()
		frames.frame_stack.append(frames.tmp_frame)
		frames.tmp_frame = None

	elif instruction.name == 'POPFRAME':

		try:
			frames.tmp_frame = frames.frame_stack[LF_len()]
		except IndexError:
			print("Empty Temp frame", file=sys.stderr)
			exit(55)
		else:
			frames.tmp_frame = frames.frame_stack[LF_len()]

		to_TF()
		del frames.frame_stack[LF_len()]

	elif instruction.name == 'PUSHS':

		if check_type_var(0):
			var_indx = var_find_index(0)
			val = find_var(get_frame(0), var_indx)
			stack_list = [val[1], val[2]]
			frames.stack.append(stack_list)
			val.pop(2)
			val.pop(1)

		else:
			frames.stack.append([instruction.args[0].type, instruction.args[0].value])

	elif instruction.name == 'POPS':
		if len(frames.stack) == 0:
			print("Empty stack frame", file=sys.stderr)
			exit(56)

		insert_into_var(
			get_frame(0),
			var_find_index(0),
			frames.stack[len(frames.stack) - 1][0],
			frames.stack[len(frames.stack) - 1][1]
		)
		del frames.stack[len(frames.stack) - 1]

	elif instruction.name == 'ADD':
		to_var_indx = var_find_index(0)

		if check_same_type(get_type(1), get_type(2)) != 'int':
			print("Incorrect type", file=sys.stderr)
			exit(53)

		if check_type_var(1):
			from_var1_indx = var_find_index(1)
			val1 = arithm_oper(1, from_var1_indx)
		else:
			val1 = instruction.args[1].value

		if check_type_var(2):
			from_var2_indx = var_find_index(2)
			val2 = arithm_oper(2, from_var2_indx)
		else:
			val2 = instruction.args[2].value

		try:
			str(int(val1) + int(val2))
		except ValueError:
			print("Invalid int value", file=sys.stderr)
			exit(32)

		insert_into_var(get_frame(0), to_var_indx, 'int', str(int(val1) + int(val2)))

	elif instruction.name == 'SUB':
		to_var_indx = var_find_index(0)

		if check_same_type(get_type(1), get_type(2)) != 'int':
			print("Incorrect type", file=sys.stderr)
			exit(53)

		if check_type_var(1):
			from_var1_indx = var_find_index(1)
			val1 = arithm_oper(1, from_var1_indx)
		else:
			val1 = instruction.args[1].value

		if check_type_var(2):
			from_var2_indx = var_find_index(2)
			val2 = arithm_oper(2, from_var2_indx)
		else:
			val2 = instruction.args[2].value

		try:
			str(int(val1) - int(val2))
		except ValueError:
			print("Invalid int type", file=sys.stderr)
			exit(32)

		insert_into_var(get_frame(0), to_var_indx, 'int', str(int(val1) - int(val2)))

	elif instruction.name == 'MUL':
		to_var_indx = var_find_index(0)

		if check_same_type(get_type(1), get_type(2)) != 'int':
			print("Incorrect type", file=sys.stderr)
			exit(53)

		if check_type_var(1):
			from_var1_indx = var_find_index(1)
			val1 = arithm_oper(1, from_var1_indx)
		else:
			val1 = instruction.args[1].value

		if check_type_var(2):
			from_var2_indx = var_find_index(2)
			val2 = arithm_oper(2, from_var2_indx)
		else:
			val2 = instruction.args[2].value

		try:
			str(int(val1) * int(val2))
		except ValueError:
			print("Invalid int type", file=sys.stderr)
			exit(32)

		insert_into_var(get_frame(0), to_var_indx, 'int', str(int(val1) * int(val2)))

	elif instruction.name == 'IDIV':
		to_var_indx = var_find_index(0)

		if check_same_type(get_type(1), get_type(2)) != 'int':
			print("Incorrect type", file=sys.stderr)
			exit(53)

		if check_type_var(1):
			from_var1_indx = var_find_index(1)
			val1 = arithm_oper(1, from_var1_indx)
		else:
			val1 = instruction.args[1].value

		if check_type_var(2):
			from_var2_indx = var_find_index(2)
			val2 = arithm_oper(2, from_var2_indx)
		else:
			val2 = instruction.args[2].value

		try:
			str(int(val1) // int(val2))
		except ValueError:
			print("Invalid int type", file=sys.stderr)
			exit(32)

		except ZeroDivisionError:
			print("Division by zero", file=sys.stderr)
			exit(57)

		insert_into_var(get_frame(0), to_var_indx, 'int', str(int(val1) // int(val2)))

	elif instruction.name == 'AND':
		to_var_indx = var_find_index(0)

		check_same_type(get_type(1), get_type(2))

		val1 = get_val(1)

		val2 = get_val(2)

		if val1 == 'true' and val2 == 'true':
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'true')
		else:
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')

	elif instruction.name == 'OR':
		to_var_indx = var_find_index(0)

		check_same_type(get_type(1), get_type(2))

		val1 = get_val(1)

		val2 = get_val(2)

		if val1 == 'false' and val2 == 'false':
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
		else:
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'true')

	elif instruction.name == 'NOT':
		to_var_indx = var_find_index(0)

		if get_type(1) != 'bool':
			print("Not same types", file=sys.stderr)
			exit(53)

		val = get_val(1)

		if val == 'true':
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
		else:
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'true')

	elif instruction.name == 'LT':
		to_var_indx = var_find_index(0)

		val1 = get_val(1)
		type1 = get_type(1)

		val2 = get_val(2)
		type2 = get_type(2)

		if type1 == 'int' and type2 == 'int':
			insert_into_var(get_frame(0), to_var_indx, 'bool', str(int(val1) < int(val2)).lower())
		elif type1 == 'bool' and type2 == 'bool':
			if val1 == 'false' and val2 == 'false':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
			elif val1 == 'false' and val2 == 'true':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'true')
			elif val1 == 'true' and val2 == 'false':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
			elif val1 == 'true' and val2 == 'true':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
		elif type1 == 'string' and type2 == 'string':
			if val1 is None:
				val1 = ''
			if val2 is None:
				val2 = ''
			insert_into_var(get_frame(0), to_var_indx, 'bool', str(val1 < val2).lower())

		elif type1 == 'nil' or type2 == 'nil':
			print("Cannot compare nil type", file=sys.stderr)
			exit(53)
		else:
			print("Invalid type", file=sys.stderr)
			exit(53)

	elif instruction.name == 'GT':
		to_var_indx = var_find_index(0)

		val1 = get_val(1)
		type1 = get_type(1)

		val2 = get_val(2)
		type2 = get_type(2)

		if type1 == 'int' and type2 == 'int':
			insert_into_var(get_frame(0), to_var_indx, 'bool', str(int(val1) > int(val2)).lower())
		elif type1 == 'bool' and type2 == 'bool':
			if val1 == 'false' and val2 == 'false':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
			elif val1 == 'false' and val2 == 'true':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
			elif val1 == 'true' and val2 == 'false':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'true')
			elif val1 == 'true' and val2 == 'true':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
		elif type1 == 'string' and type2 == 'string':
			if val1 is None:
				val1 = ''
			if val2 is None:
				val2 = ''
			insert_into_var(get_frame(0), to_var_indx, type1, str(val1 > val2).lower())

		elif type1 == 'nil' or type2 == 'nil':
			print("Cannot compare nil type", file=sys.stderr)
			exit(53)
		else:
			print("Invalid type", file=sys.stderr)
			exit(53)

	elif instruction.name == 'EQ':
		to_var_indx = var_find_index(0)

		val1 = get_val(1)
		type1 = get_type(1)

		val2 = get_val(2)
		type2 = get_type(2)
		if type1 == 'int' and type2 == 'int':
			insert_into_var(get_frame(0), to_var_indx, 'bool', str(int(val1) == int(val2)).lower())
		elif type1 == 'bool' and type2 == 'bool':
			if val1 == 'false' and val2 == 'false':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'true')
			elif val1 == 'false' and val2 == 'true':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
			elif val1 == 'true' and val2 == 'false':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
			elif val1 == 'true' and val2 == 'true':
				insert_into_var(get_frame(0), to_var_indx, 'bool', 'true')
		elif type1 == 'string' and type2 == 'string':
			if val1 is None:
				val1 = ''
			if val2 is None:
				val2 = ''
			insert_into_var(get_frame(0), to_var_indx, 'bool', str(val1 == val2).lower())

		elif type1 == 'nil' and type2 == 'nil':
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'true')

		elif type1 == 'nil' or type2 == 'nil':
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')
		else:
			print("Incorrect type", file=sys.stderr)
			exit(53)

	elif instruction.name == 'INT2CHAR':
		to_var_indx = var_find_index(0)

		if get_type(1) != 'int':
			print("Incorrect type", file=sys.stderr)
			exit(53)

		val = get_val(1)

		try:
			chr(int(val))
		except:
			print("Incorrect Unicode value", file=sys.stderr)
			exit(58)
		else:
			insert_into_var(get_frame(0), to_var_indx, 'string', chr(int(val)))

	elif instruction.name == 'STRI2INT':
		to_var_indx = var_find_index(0)

		val1 = get_val(1)
		val2 = get_val(2)

		if get_type(1) != 'string':
			print("Incorrect Unicode value", file=sys.stderr)
			exit(53)

		if get_type(2) != 'int':
			print("Incorrect type", file=sys.stderr)
			exit(53)

		if int(val2) < 0:
			print("Index out of range", file=sys.stderr)
			exit(58)

		try:
			ord(val1[int(val2)])
		except IndexError:
			print("Index out of range", file=sys.stderr)
			exit(58)
		except:
			print("Incorrect Unicode value", file=sys.stderr)
			exit(58)
		else:
			insert_into_var(get_frame(0), to_var_indx, 'int', str(ord(val1[int(val2)])))

	elif instruction.name == 'CONCAT':
		to_var_indx = var_find_index(0)

		val1 = get_val(1)
		val2 = get_val(2)

		if get_type(1) != 'string' or get_type(2) != 'string':
			print("Incorrect data type", file=sys.stderr)
			exit(53)

		if val1 is None:
			val1 = ''
		if val2 is None:
			val2 = ''

		string = val1 + val2
		insert_into_var(get_frame(0), to_var_indx, 'string', string)

	elif instruction.name == 'STRLEN':
		to_var_indx = var_find_index(0)

		val1 = get_val(1)
		type1 = get_type(1)

		if type1 != 'string':
			print("Incorrect data type", file=sys.stderr)
			exit(53)

		val1 = len(val1)

		insert_into_var(get_frame(0), to_var_indx, 'int', str(int(val1)))

	elif instruction.name == 'GETCHAR':
		to_var_indx = var_find_index(0)

		val1 = get_val(1)
		type1 = get_type(1)

		if type1 != 'string':
			print("Incorrect data type", file=sys.stderr)
			exit(53)

		val2 = get_val(2)
		type2 = get_type(2)

		if type2 != 'int':
			print("Incorrect data type", file=sys.stderr)
			exit(53)

		if int(val2) < 0:
			print("Incorrect getchar range", file=sys.stderr)
			exit(58)

		try:
			val1[int(val2)]
		except IndexError:
			print("Index out of range", file=sys.stderr)
			exit(58)
		else:
			pass

		insert_into_var(get_frame(0), to_var_indx, 'string', val1[int(val2)])

	elif instruction.name == 'SETCHAR':
		to_var_indx = var_find_index(0)
		val0 = get_val(0)
		type0 = get_type(0)

		val1 = get_val(1)
		type1 = get_type(1)
		if type1 != 'int':
			print("Incorrect data type", file=sys.stderr)
			exit(53)

		val2 = get_val(2)

		if int(val1) < 0 or int(val1) >= len(val0):
			print("Index out of range", file=sys.stderr)
			exit(58)

		if val2 == '':
			print("Empty string")
			exit(58)

		type2 = get_type(2)

		if type0 != 'string' or type2 != 'string':
			print("Incorrect data type", file=sys.stderr)
			exit(53)

		val0 = val0[:int(val1)] + val2[0] + val0[int(val1)+1:]
		insert_into_var(get_frame(0), to_var_indx, 'string', val0)

	elif instruction.name == 'TYPE':
		to_var_indx = var_find_index(0)

		try:
			get_type(1)
		except TypeError:
			insert_into_var(get_frame(0), to_var_indx, 'string', '')
		else:
			insert_into_var(get_frame(0), to_var_indx, 'string', get_type(1))

	elif instruction.name == 'EXIT':
		val = get_val(0)

		if get_type(0) != 'int':
			print("Invalid type ", file=sys.stderr)
			exit(53)

		if int(val) > 49 or int(val) < 0:
			print("Invalid exit code " + val, file=sys.stderr)
			exit(57)

		exit(int(val))
		break

	elif instruction.name == 'DPRINT':
		val = get_val(0)
		print(val, file=sys.stderr)

	elif instruction.name == 'BREAK':
		print("FUNCTION ORDER:", child[i].get(key='order'), file=sys.stderr)
		print("GLOBAL: ", frames.global_frame, file=sys.stderr)
		print("LOCAL: ", frames.frame_stack, file=sys.stderr)
		print("TEMP: ", frames.tmp_frame, file=sys.stderr)
		print("STACK:", frames.stack, file=sys.stderr)
		print("LABELS:", frames.labels, file=sys.stderr)
		print("CALL_STACK:", frames.call_stack, file=sys.stderr)

	i += 1

	# print("GLOBAL: ", frames.global_frame, file=sys.stderr)
	# print("LOCAL: ", frames.frame_stack, file=sys.stderr)
	# print("TEMP: ", frames.tmp_frame, file=sys.stderr)
	# print("STACK:", frames.stack, file=sys.stderr)
	# print("LABELS:", frames.labels, file=sys.stderr)
	# print("CALL_STACK:", frames.call_stack, file=sys.stderr)
	# print("FUNCTIONS: read operands:", len(instruction.args), "\n", file=sys.stderr)
