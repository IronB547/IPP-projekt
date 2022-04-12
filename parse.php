<?php
# Principy programovacích jazyků a OOP (IPP)
# Author: Tomáš Dvořák 
# Login: xdvora3r

ob_start(); # Function to not print already "generated" XML code to STDIN.
define('function_name', '0');

ini_set('display_errors', 'stderr');
echo("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")."\n";

# BEGINNING of functions.
# Error functions for handling errors.
function header_error() { # Incorrect header.
	ob_end_clean(); # This will silence the already "generated" XML code.
	#echo "Error 21\n";
	exit(21);
}

function incorrect_function_error() { # Incorrect function name.
	ob_end_clean(); # This will silence the already "generated" XML code.
	#echo "Error 22\n";
	exit(22);
}

function other_error() { # Basically anything else.
	#ob_end_clean(); # This will silence the already "generated" XML code.
	echo "Error 23\n";
	exit(23);
}

# I couldn't use one singular function or many together, it wouldn't work the way I wanted to.
# I hope I haven't reinvented the wheel, but this fuction works properly without errors.
function remove_spaces($input) { # Function that removes ' ' and '\t' from the code.
	$var_flag = false;
	$len = strlen($input);

	for($i = 0; $i < $len; $i++) {

		if(($input[$i] == ' ' ) && $var_flag) { # Replace first empty space/tab after any character (end of operand) with '|'.
			$input[$i] = '|';
			$var_flag = false; # Set flag to false. We are reading ' ' and/or '\t'.
		}
		else if($input[$i] != ' ' && $input[$i] != "\t") # If you read a part of a code (any character), set to true.
			$var_flag = true;
	}

	$input = str_replace(' ', '', $input); # Replace ' ' and 't' with empty string.
	$input = str_replace("\t", '', $input);
	$input = rtrim($input, '|'); # If there's a tab or space behind the code there will be a '|' at the end, so cut it away.
	return $input; # E.g: DEFVAR|GF@a or MOVE|GF@a|int@25.
}

# Simple function that returns value after '@' symbol.
# $cut is an array that has a function and its operands. e.g.: $cut[0] == DEFVAR $cut[1] == GF@abc
# $param is a static number, used for selection of the operand the function is working with.
function get_val($cut, $param) {

	if(str_contains($cut[$param], "@")) { # If value after '@' is empty, throw exception
		$value = htmlspecialchars($cut[$param]); # Conversion for strings.
		$value = explode('@', $value); # Separate values. e.g. DEFVAR GF@abc -> value[0] == GF value[1] == abc

		return $value[1]; # Return value after '@' ([1] because I want the second value in GF@abc).
	}
	else { # If operand does not contain '@' symbol, throw exception.
		other_error();
	}
}

# Function prints out the value any of the following: variable, int, bool, string and nil.
# $cut is an array that has a function and its operands. e.g.: $cut[0] == DEFVAR $cut[1] == GF@abc
# $value is the value of an operand after '@' symbol.
# $param is a static number, used for selection of the operand the function is working with.
# e.g.: MOVE GF@abc int@25 -> readval($cut, get_val($cut, 1), 1) will be working with the first operand and value abc.
function determine_val($cut, $value, $param) { # The core of this script.

	if(!preg_match("~\bstring\b~", $cut[$param])) { # If not an empty string, but still are empty, throw exception.
		if(empty($value) && $value != 0)
			other_error();
	}
	
	# Big if else tree.
	if(preg_match("/(GF|LF|TF)@[a-zA-Z#$&*_%!?][a-zA-Z#$&*_%!?0-9]*/", $cut[$param])) # Print argument if variable.
		echo("\t\t<arg$param type=\"var\">$cut[$param]</arg$param>")."\n";

	else if(preg_match("~\bint\b~", $cut[$param])) # Print argument if int.
		if(preg_match('/^(\+|-|)(0[xX][0-9a-fA-F]+|0b[0-1]+|(0[oO]|0)[0-7]+\b|[0-9]+)\b/', $value)) { # Check for hex, oct, bin and normal numbers
			echo("\t\t<arg$param type=\"int\">$value</arg$param>")."\n";
		}
		else
			other_error();

	else if(preg_match("~\bbool\b~", $cut[$param])) {  # Print argument if bool.
		$value = strtolower($value); # Accept TRUE or true.

		if(str_contains($value, "true") || str_contains($value, "false")) # Only accept true/false, not 0 or 1.
			echo("\t\t<arg$param type=\"bool\">$value</arg$param>")."\n";
		else
			other_error();
	}

	else if(preg_match("~\bstring\b~", $cut[$param])) {  # Print argument if string.
		
		# Another manually implemented "function". Couldn't find anything that would help me
		# so I've created my own function. It checks for correct escape sequences.
		if(str_contains($value, "\\")) { # If string has a '\' check for any numbers after '\'.

			$total = substr_count($value, "\\"); # Total amount of "\" 
			$string = explode('\\', $value); # Take values after "\"
			$len = sizeof($string); # Total amount of cells in $string
			$count = 0; # counter

			for($i = 1; $i < $len; $i++) {
				$check = str_split($string[$i]);
				$arr = str_split($string[$i], 3); # Take first three characters after "\".


				if(preg_match('/^([0-9]{3})\b/', $arr[0])) # If three numbers were read, counter++
					$count++;
				else if(empty($string[$i]) && $count != $total && !str_contains($string[$i], "0")) # Accept "\000" and empty "\" (nothing after the "\")
					$count++;
			}

			if($count == $total) # if counter == total amount of "\" -> success
				echo("\t\t<arg$param type=\"string\">$value</arg$param>")."\n";
			else # else -> failed
				other_error();
		}

		else # If no '\' is present, just go ahead and print.
			echo("\t\t<arg$param type=\"string\">$value</arg$param>")."\n";		
	}

	else if(preg_match("~\bnil@nil\b~", $cut[$param])) # Print argument if nil.
		echo("\t\t<arg$param type=\"nil\">$value</arg$param>")."\n";

	else # if anything else, error.
		other_error();
}

# Simple instruction print just to make the code more readable.
# $instruction is the amount of read functions (IPPcode22), used for instruction order.
# $cut is an array that has a function and its operands. e.g.: $cut[0] == DEFVAR $cut[1] == GF@abc
function print_instruction($instruction, $cut) { 
	echo("\t<instruction order=\"".$instruction."\" opcode=\"".strtoupper($cut[function_name])."\">\n");
}

# Same as above, however at the end there's /> for one line functions like CREATEFRAME, PUSHFRAME...
function print_instruction_short($instruction, $cut) { 
	echo("\t<instruction order=\"".$instruction."\" opcode=\"".strtoupper($cut[function_name])."\" />\n");
}

# Simple function that checks how many operands were inserted, compared to how many should be present
# $cut is an array that has a function and its operands. e.g.: $cut[0] == DEFVAR $cut[1] == GF@abc
# $allowed is just like $param. Static number that is used for checking total operand count.
function check_ops($cut, $allowed) { 
	if(sizeof($cut) - 1 != $allowed)
		other_error();
}

 # Function that checks only for variables (usually the first operand).
 # $cut is an array that has a function and its operands. e.g.: $cut[0] == DEFVAR $cut[1] == GF@abc
function var_only($cut) {
	if(preg_match("/(GF|LF|TF)@[a-zA-Z#$&*_%!?][a-zA-Z#$&*_%!?0-9]*/", $cut[1])) # The first operand MUST be var.
		echo("\t\t<arg1 type=\"var\">$cut[1]</arg1>")."\n"; 					 # Example: DEFVAR|GF@a -> $cut[1] == GF@a.
	else
		other_error();
}

# Constant repeating of these throughout the entire code. Made this so the code is more readable. Most functions became a one liner with this.
# $cut is an array that has a function and its operands. e.g.: $cut[0] == DEFVAR $cut[1] == GF@abc
# $instruction is the amount of read functions (IPPcode22), used for instruction order.
# $param is a static number, used for selection of the operand the function is working with.
function function_print($cut, $instruction, $param) { 
	check_ops($cut, $param); # Check for allowed operands, any more or less, throw an exception.

	print_instruction($instruction, $cut); # Print the instruction.

	var_only($cut); # First operand MUST be var.

	if($param == 3) { # Either one operand or two operands are present.
		determine_val($cut, get_val($cut, $param - 1), $param - 1); # Insert any second operand.
		determine_val($cut, get_val($cut, $param), $param); # Insert any second operand.
	}
	else
		determine_val($cut, get_val($cut, $param), $param); # Insert any second operand.

	echo "\t</instruction>\n"; # Print end of instruction.
}
# END of functions.

if ($argc > 1) { # Prints --help.
	if (preg_match("/^--help$/", $argv[1]) && $argc == 2) {
		ob_end_clean();
		echo "Parser usage:"."\n\n";
		echo "Filter type script reads source code (IPPcode22) from STDIN, does a lexical\nand syntax check and prints out to STDOUT an XML representation.\n";
		echo 'You can use parse.php with "--help" parameter to print this message.'."\n";
		exit(0);
	}
	else {
		ob_end_clean();
		exit(10);
	}
}

# BEGINNING of script.
$header = false; 
$instruction = 0; # Start from 0, read .IPPcode22 and count it as 1.


while(($input = fgets(STDIN)) !== false) { # Read STDIN until we reach the end.

	 # Removes comments from code. Used once and too small to be it's own function.
	if(str_contains($input, "#")) {
		$comment = explode('#', trim($input, "\n"));
		$input = $comment[0];  # Anything after a '#' will be ignored, even multiple "#" symbols are ignored by static [0].
	}

	$input = trim($input, "\n"); # Remove new line at end of string.
	$input = remove_spaces($input); # Create '|' delimiters and remove spaces and tabs.

	if(!$header && !empty($input)) { # At first, we need to read .IPPcode22.
		$input = strtoupper($input); # Accept any variant of .IPPcode22.
				
		if(preg_match('/^( *)\.IPPCODE22\b/', $input)) { # If .IPPcode22, set header to true and continue.
			$header = true;
			$input = NULL; # Remove .IPPcode22 (script would think it's a function).
			echo("<program language=\"IPPcode22\">\n");
		}

		else { # If all fails, that must mean no header is present. Throw exception.
			header_error();
		}
	}

	$cut = explode('|', $input); # Cut $input into individuals segments.
	$value; # Values of operands will be inserted here.

	if(!($input == "\n") && !empty($input) ) { # If the line is not empty and it's not a new line, instruction_counter++.
		$instruction++;
		}

	# BEGINNING of the switch.
	switch(strtoupper($cut[function_name])) { # Determine function and what to do with it.
		# All of these are made out of functions that are described above.
		# There's only a few functions that have their own code. They are commented as well.

		case 'DEFVAR':
			check_ops($cut, 1);

			print_instruction($instruction, $cut);

			var_only($cut);

			echo "\t</instruction>\n";
			break;

		case 'CREATEFRAME':
			check_ops($cut, 0);
			print_instruction_short($instruction, $cut);
			break;

		case 'PUSHFRAME':
			check_ops($cut, 0);
			print_instruction_short($instruction, $cut);
			break;

		case 'POPFRAME':
			check_ops($cut, 0);
			print_instruction_short($instruction, $cut);
			break;

		case 'BREAK':
			check_ops($cut, 0);
			print_instruction_short($instruction, $cut);
			break;

		case 'RETURN':
			check_ops($cut, 0);
			print_instruction_short($instruction, $cut);
			break;

		case 'PUSHS':
			check_ops($cut, 1);
			print_instruction($instruction, $cut);

			determine_val($cut, get_val($cut, 1), 1);

			echo "\t</instruction>\n";
			break;

		case 'POPS':
			check_ops($cut, 1);
			print_instruction($instruction, $cut);

			var_only($cut);

			echo "\t</instruction>\n";
			break;

		case 'EXIT':
			check_ops($cut, 1);

			print_instruction($instruction, $cut);
			$value = get_val($cut, 1);

			determine_val($cut, $value, 1, 1);

			echo "\t</instruction>\n";
			break;

		case 'DPRINT':
			check_ops($cut, 1);

			print_instruction($instruction, $cut);
			$value = get_val($cut, 1);

			if(preg_match("~\bint\b~", $cut[1])) # Only int is accepted.
				if (preg_match('/^([0-9]+)\b/', $value))
					echo("\t\t<arg1 type=\"int\">$value</arg1>")."\n";
				else
					other_error();
			else
				other_error();

			echo "\t</instruction>\n";
			break;

		case 'READ':
			check_ops($cut, 2);

			print_instruction($instruction, $cut);

			var_only($cut);

			# Same with determine_val, but the arg type is 'type'.
			if(preg_match("~\bint\b~", $cut[2])) 
				echo("\t\t<arg2 type=\"type\">$cut[2]</arg2>")."\n";

			else if(preg_match("~\bbool\b~", $cut[2]))
				echo("\t\t<arg2 type=\"type\">$cut[2]</arg2>")."\n";

			else if(preg_match("~\bstring\b~", $cut[2]))
				echo("\t\t<arg2 type=\"type\">$cut[2]</arg2>")."\n";

			else
				echo("\t\t<arg2 type=\"type\">nil</arg2>")."\n";

			echo "\t</instruction>\n";
			break;

		case 'WRITE':
			check_ops($cut, 1);
			$value = htmlspecialchars($cut[1]); # Library function to convert <, >, & and other characters into HTLM.

			$value = get_val($cut, 1);

			print_instruction($instruction, $cut);

			determine_val($cut, $value, 1, 1);

			echo "\t</instruction>\n";
			break;

		case 'CALL':
			check_ops($cut, 1);

			if(!empty($cut[1])) # If $value is empty, throw exception.
				$value = htmlspecialchars($cut[1]);
			else
				other_error();

			print_instruction($instruction, $cut);

			if(!str_contains($value, "@")) # Simple label check, it cannot contain '@' value.
				echo("\t\t<arg1 type=\"label\">$value</arg1>")."\n";
			else
				other_error();

			echo "\t</instruction>\n";
			break;

		case 'LABEL':
			check_ops($cut, 1);

			if(!empty($cut[1])) # Same as in CALL, if empty, throw exception.
				$value = htmlspecialchars($cut[1]);
			else
				other_error();

			print_instruction($instruction, $cut);

			if(!str_contains($value, "@")) # LABEL cannot have '@' symbol.
				echo("\t\t<arg1 type=\"label\">$value</arg1>")."\n";
			else
				other_error();

			echo "\t</instruction>\n";
			break;

		case 'JUMP':
			check_ops($cut, 1);

			if(!empty($cut[1])) # if empty, throw exception.
				$value = htmlspecialchars($cut[1]);
			else
				other_error();

			print_instruction($instruction, $cut);

			if(!str_contains($value, "@")) # LABEL cannot have '@' symbol.
				echo("\t\t<arg1 type=\"label\">$value</arg1>")."\n";
			else
				other_error();

			echo "\t</instruction>\n";
			break;

		case 'JUMPIFEQ':
			check_ops($cut, 3);

			if(!empty($cut[1]))
				$value = htmlspecialchars($cut[1]);
			else
				other_error();

			print_instruction($instruction, $cut);

			if(!str_contains($value, "@")) # First MUST be label, then operands.
				echo("\t\t<arg1 type=\"label\">$value</arg1>")."\n";
			else
				other_error();

			determine_val($cut, get_val($cut, 2), 2); 

			determine_val($cut, get_val($cut, 3), 3); 

			echo "\t</instruction>\n";
			break;

		case 'JUMPIFNEQ':
			check_ops($cut, 3);

			if(!empty($cut[1]))
				$value = htmlspecialchars($cut[1]);
			else
				other_error();

			print_instruction($instruction, $cut);

			if(!str_contains($value, "@")) # First MUST be label, then operands.
				echo("\t\t<arg1 type=\"label\">$value</arg1>")."\n";
			else
				other_error();

			determine_val($cut, get_val($cut, 2), 2); 

			determine_val($cut, get_val($cut, 3), 3); 
			
			echo "\t</instruction>\n";
			break;

		#Beginning of one liner functions.
		case 'MOVE':
			function_print($cut, $instruction, 2);
			break;

		case 'LT':

			function_print($cut, $instruction, 3);
			break;

		case 'GT':

			function_print($cut, $instruction, 3);
			break;
			
		case 'EQ':
			
			function_print($cut, $instruction, 3);
			break;

		case 'TYPE':
			
			function_print($cut, $instruction, 2);
			break;

		case 'ADD':
			
			function_print($cut, $instruction, 3);
			break;

		case 'SUB':

			function_print($cut, $instruction, 3);
			break;

		case 'MUL':
			
			function_print($cut, $instruction, 3);
			break;

		case 'IDIV':
			
			function_print($cut, $instruction, 3);
			break;

		case 'AND':
			
			function_print($cut, $instruction, 3);
			break;

		case 'OR':
			
			function_print($cut, $instruction, 3);
			break;

		case 'NOT':
			
			function_print($cut, $instruction, 2);
			break;

		case 'STRI2INT':
				
			function_print($cut, $instruction, 3);
			break;

		case 'CONCAT':
				
			function_print($cut, $instruction, 3);
			break;

		case 'INT2CHAR':
			
			function_print($cut, $instruction, 2);
			break;

		case 'STRLEN':
			
			function_print($cut, $instruction, 2);
			break;

		case 'GETCHAR':
				
			function_print($cut, $instruction, 3);
			break;

		case 'SETCHAR':
			
			function_print($cut, $instruction, 3);
			break;

		default: # If none of the functions above were read, throw exception.
			if(!empty($cut[function_name])) {
				incorrect_function_error();
			}
			break;
		# END of switch
	}
}
	# Print end of program.
	echo ("</program>\n");
	exit(0);
	# END of script.
	# Hooray, we've reached the end without errors! Thank you for reading :).
?>