import argparse
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

			self.frame_stack[len(self.frame_stack) - 1].append([var_name])

		if f_type == "TF":
			if self.tmp_frame == None:
				print("No TF created")
				exit(55)

			self.tmp_frame.append([var_name])

	def search_frame(self, f_type, var_name):
		var_counter = 0
		if f_type == "GF":
			for variable in range(len(self.global_frame)):
				#print(self.global_frame[variable][0], var_name)
				if var_name == self.global_frame[variable][0]:
					var_counter += 1
					#print(var_counter)

			if instruction.name == 'DEFVAR' and var_counter == 1:
				print("Redeclaration of variable: " + var_name)
				exit(52) # Check for correct error TODO
			elif instruction.name != 'DEFVAR' and var_counter == 0:
				print("Variable " + var_name + " doesn't exist.")
				exit(52) # Check for correct error TODO

		elif f_type == "LF":
			for variable in range(len(self.frame_stack)):
				if var_name == self.frame_stack[LF_len()][variable]:
					var_counter += 1

			if instruction.name == 'DEFVAR' and var_counter == 1:
				print("Redeclaration of variable: " + var_name)
				exit(52) # Check for correct error TODO
			elif instruction.name != 'DEFVAR' and var_counter == 0:
				print("Variable " + var_name + " doesn't exist.")
				exit(52) # Check for correct error TODO

		elif f_type == "TF":
			for variable in range(len(self.tmp_frame)):
				if var_name == self.tmp_frame[variable][0]:
					var_counter += 1

			if instruction.name == 'DEFVAR' and var_counter == 1:
				print("Redeclaration of variable: " + var_name)
				exit(52) # Check for correct error TODO
			elif instruction.name != 'DEFVAR' and var_counter == 0:
				print("Variable " + var_name + " doesn't exist.")
				exit(52) # Check for correct error TODO

	def return_index(self, f_type, var_name):
		index = 0
		if f_type == "GF":
			for variable in range(len(self.global_frame)):
				if var_name == self.global_frame[variable][0]:
					return index
				index += 1

		elif f_type == "LF":
			for variable in range(len(self.frame_stack[len(self.frame_stack) - 1])):
				if var_name == self.frame_stack[LF_len()][variable][0]:
					return index
				index += 1

		elif f_type == "TF":
			for variable in range(len(self.tmp_frame)):
				if var_name == self.tmp_frame[variable][0]:
					return index
				index += 1
		print(index)
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

def check_var_type(arg_num):
	if instruction.args[arg_num].type == 'var':
		return True
	else:
		return False

def LF_len():
	return len(frames.frame_stack) - 1

def to_LF():
	for variable in frames.tmp_frame:
		new_var = variable[0].partition("@")
		new_var = list(new_var)
		new_var[0] = 'LF'
		new_var = "".join(new_var)

		variable[0] = new_var

def	to_TF():
	for variable in frames.tmp_frame:
		new_var = variable[0].partition("@")
		new_var = list(new_var)
		new_var[0] = 'TF'
		new_var = "".join(new_var)

		variable[0] = new_var

def var_find_index(argument_num):
	if frames.return_index(get_frame(argument_num), instruction.args[argument_num].value) == None:
		print("Non defined variable " + instruction.args[argument_num].value)
		exit(54)

	return frames.return_index(get_frame(argument_num), instruction.args[argument_num].value)

def find_var(frame, from_var_indx):
	if frame == 'GF':
		if len(frames.global_frame[from_var_indx]) > 1:
			return frames.global_frame[from_var_indx]
		else:
			print("Variable " + frames.global_frame[from_var_indx][0] + " is empty.")
			exit(54) # Check for correct exit code TODO

	elif frame == 'LF':
		if len(frames.frame_stack[LF_len()][from_var_indx]) > 1:
			return frames.frame_stack[LF_len()][from_var_indx]
		else:
			print("Variable " + frames.frame_stack[LF_len()][from_var_indx][0] + " is empty.")
			exit(54) # Check for correct exit code TODO

	elif frame == 'TF':
		if len(frames.tmp_frame[from_var_indx]) > 1:
			return frames.tmp_frame[from_var_indx]
		else:
			print("Variable " + frames.tmp_frame[from_var_indx][0] + " is empty.")
			exit(54) # Check for correct exit code TODO

def insert_into_var(frame, to_var_indx, from_type, from_value):
	if frame == 'GF':
		if len(frames.global_frame[to_var_indx]) > 1:
			frames.global_frame[to_var_indx][1] = from_type
			frames.global_frame[to_var_indx][2] = from_value
		else:
			frames.global_frame[to_var_indx].append(from_type)
			frames.global_frame[to_var_indx].append(from_value)

	elif frame == 'LF':
		if len(frames.frame_stack[len(frames.frame_stack) - 1][to_var_indx]) > 1:
			frames.frame_stack[LF_len()][to_var_indx][1] = from_type
			frames.frame_stack[LF_len()][to_var_indx][2] = from_value
		else:
			frames.frame_stack[LF_len()][to_var_indx].append(from_type)
			frames.frame_stack[LF_len()][to_var_indx].append(from_value)
	elif frame == 'TF':
		if len(frames.tmp_frame[to_var_indx]) > 1:
			frames.tmp_frame[to_var_indx][1] = from_type
			frames.tmp_frame[to_var_indx][2] = from_value
		else:
			frames.tmp_frame[to_var_indx].append(from_type)
			frames.tmp_frame[to_var_indx].append(from_value)

def arithm_oper(arg_num, from_var_indx):
	val = None
	val = find_var(get_frame(arg_num), from_var_indx)
	if val[1] == 'int':
		val = val[2]
	else:
		print("Incorrect type " + val[1])
		exit(53)  # Check for correct exit code TODO

	return val

def logic_oper(arg_num, from_var_indx):
	val = None
	val = find_var(get_frame(arg_num), from_var_indx)
	if val[1] == 'bool':
		val = val[2]
	else:
		print("Incorrect type " + instruction.args[arg_num].type)
		exit(53)  # Check for correct exit code TODO

	return val

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

	elif instruction.name == 'MOVE':
		frames.search_frame(get_frame(0), instruction.args[0].value)

		to_var_indx = var_find_index(0)
		if instruction.args[1].type != 'var': # check if second argument is variable or not
			insert_into_var(get_frame(0), to_var_indx, instruction.args[1].type, instruction.args[1].value)
		else:
			frames.search_frame(get_frame(1), instruction.args[1].value)
			from_var_indx = var_find_index(1)
			type = find_var(get_frame(1), from_var_indx)
			value = find_var(get_frame(1), from_var_indx)

			insert_into_var(get_frame(0), to_var_indx, type[1], value[2])

	elif instruction.name == 'WRITE':
		to_var_indx = var_find_index(0)
		if get_frame(0) == 'GF':
			if len(frames.global_frame[to_var_indx]) > 1:
				print(frames.global_frame[to_var_indx][2], end='')
			else:
				print("Variable: "+ frames.global_frame[to_var_indx][0] +" is empty")
				exit(53) # Check correct exit code TODO

		elif get_frame(0) == 'LF':
			if len(frames.frame_stack[LF_len()][to_var_indx]) > 1:
				print(frames.frame_stack[LF_len()][to_var_indx][2], end='')
			else:
				print("Variable: "+ frames.frame_stack[len(frames.frame_stack) - 1][to_var_indx][0] +" is empty")
				exit(53) # Check correct exit code TODO

		elif get_frame(0) == 'TF':
			if len(frames.tmp_frame[to_var_indx]) > 1:
				print(frames.tmp_frame[to_var_indx][2], end='')
			else:
				print("Variable: "+ frames.tmp_frame[to_var_indx][0] +" is empty")
				exit(53) # Check correct exit code TODO

		print() # TO BE DELETED, JUST FOR BETTER PRINTS

	elif instruction.name == 'CREATEFRAME':
		frames.tmp_frame = []

	elif instruction.name == 'PUSHFRAME':
		to_LF()
		if frames.tmp_frame != None:
			frames.frame_stack.append(frames.tmp_frame)
			frames.tmp_frame = None
		else:
			print("Empty Temp frame.")
			exit(53) # Check for correct exit code TODO

	elif instruction.name == 'POPFRAME':
		frames.tmp_frame = frames.frame_stack[LF_len()]
		to_TF()
		del frames.frame_stack[LF_len()]

	elif instruction.name == 'PUSHS':

		if(check_var_type(0)):
			var_indx = var_find_index(0)
			val = find_var(get_frame(0), var_indx)
			list = [val[1], val[2]]
			frames.stack.append(list)
			val.pop(2)
			val.pop(1)

		else:
			frames.stack.append([instruction.args[0].type, instruction.args[0].value])

	elif instruction.name == 'POPS':

		insert_into_var(get_frame(0), var_find_index(0), frames.stack[len(frames.stack) - 1][0], frames.stack[len(frames.stack) - 1][1])
		del frames.stack[len(frames.stack) - 1]

	elif instruction.name == 'ADD':
		to_var_indx = var_find_index(0)

		from_var1_indx = var_find_index(1)
		val1 = arithm_oper(1, from_var1_indx)

		from_var2_indx = var_find_index(2)
		val2 = arithm_oper(2, from_var2_indx)

		insert_into_var(get_frame(0), to_var_indx, 'int', int(val1) + int(val2))

	elif instruction.name == 'SUB':
		to_var_indx = var_find_index(0)

		from_var1_indx = var_find_index(1)
		val1 = arithm_oper(1, from_var1_indx)

		from_var2_indx = var_find_index(2)
		val2 = arithm_oper(2, from_var2_indx)

		insert_into_var(get_frame(0), to_var_indx, 'int', int(val1) - int(val2))

	elif instruction.name == 'MUL':
		to_var_indx = var_find_index(0)

		from_var1_indx = var_find_index(1)
		val1 = arithm_oper(1, from_var1_indx)

		from_var2_indx = var_find_index(2)
		val2 = arithm_oper(2, from_var2_indx)

		insert_into_var(get_frame(0), to_var_indx, 'int', int(val1) * int(val2))

	elif instruction.name == 'IDIV':
		to_var_indx = var_find_index(0)

		from_var1_indx = var_find_index(1)
		val1 = arithm_oper(1, from_var1_indx)

		from_var2_indx = var_find_index(2)
		val2 = arithm_oper(2, from_var2_indx)

		if val2 == 0:
			print("Division by 0")
			exit(57)

		insert_into_var(get_frame(0), to_var_indx, 'int', int(val2) // int(val1))

	elif instruction.name == 'AND':
		to_var_indx = var_find_index(0)

		if check_var_type(1):
			from_var1_indx = var_find_index(1)
			val1 = logic_oper(1, from_var1_indx)
		else:
			val1 = instruction.args[1].value

		if check_var_type(2):
			from_var2_indx = var_find_index(2)
			val2 = arithm_oper(2, from_var2_indx)
		else:
			val2 = instruction.args[2].value

		if val1 == 'true' and val2 == 'true':
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'true')
		else:
			insert_into_var(get_frame(0), to_var_indx, 'bool', 'false')

	#elif instruction.name == 'OR':

	#elif instruction.name == 'NOT:

	elif instruction.name == 'JUMP':
		print("I read jump!")

	# len(instruction.args), instruction.name
	print("GLOBAL: ", frames.global_frame)
	print("LOCAL: ", frames.frame_stack)
	print("TEMP: ", frames.tmp_frame)
	print("STACK:", frames.stack)
	print("FUNCTIONS: read operands:", len(instruction.args), "\n")
