<?php
# Principy programovacích jazyků a OOP (IPP)
# test.php
# Author: Tomáš Dvořák 
# Login: xdvora3r

# Using the ob_start and ob_end_clean functions for simpler printing.
ob_start();

# Echoing the HTML to STDOUT. Errors are handled with error_log.
# Printing the head of every HTML that will be generated.
echo('<!DOCTYPE html>
<html>
	<head>
		<style>

			table {
				border: 3px solid black;
				border-radius: 10px;
			}

			th {
				background-color: #5c5c5c;
				border-radius: 5px;
				text-align-last: center;
			}

			td{
				background-color: #6b6b6b;
				border-radius: 5px;
				text-align-last: center;
			}

		</style>
	</head>
	<body style="background-color:#737373; font-family: Arial, sans-serif; ">');

# Default configuration of test script.
$int_only = false;
$parse_only = false;
$both = true;
$rec_search = false;
$noclean = false;

# Default paths for test script.
$parse_path = "./parse.php";
$int_path = "./interpret.py";
$test_path = "./";
$xml_lib_path = "/pub/courses/ipp/jexamxml/jexamxml.jar";
$xml_lib_options = "/pub/courses/ipp/jexamxml/options";

# print error - Function for printing error messages.
# Takes the message as input and prints it to STDERR.
# Throws an exception.
function print_error($message) {
	error_log($message);
	ob_end_clean();	
	exit(41);
}

# help_print - Function that handles printing help.
function help_print() {
	ob_end_clean();	
	echo "Default settings:\n";
	echo "\tTest script assumes both Interpreter and Parser are used\n";
	echo "\tScript looks only in current directory for tests\n";
	echo "Usage of the test script:\n";
	echo "\t--help\t\t\tPrints this message\n";
	echo "\t--directory='path'\tSet path of the test directory\n";
	echo "\t--recursive\t\tTests will be run from the main directory as well as all subdirectories\n";
	echo "\t--parse-script='file'\tPath to parser, default location is './parse.php'\n";
	echo "\t--int-script=file\tPath to interpreter, default location is './interpret.php'\n";
	echo "\t--parse-only\t\tTest only the parser\n";
	echo "\t--int-only\t\tTest only the interpreter\n";
	echo "\t--jexampath='path'\tPath to JExamXML dir containing java executable and its options file\n";
	echo "\t--noclean\t\tDisables cleaning temporary files created for comparing results\n";
	exit(0);
}

# file_iteration - Function returns a file iterator according to configuration.
# $rec_search = bool, either return recursive or normal iterator.
# $test_path = either default, or --directory path.
# Function returns a file iterator, that is used to iterate through files in directories.
function file_iteration($rec_search, $test_path) {

	if($rec_search)
		return new RecursiveIteratorIterator(
					new RecursiveDirectoryIterator($test_path));
	else
		return new RecursiveDirectoryIterator($test_path);
}

# check_default_files - Function checks if files '.in', '.out' and '.rc' exist, if not, create them.
# $file = source file that must exist in order to create said files.
# $path = path to the directory where you create the default files.
function check_default_files($file, $path) {

	if(!file_exists($check_file = $path . $file . ".in")) {
		$create_default_file = fopen($check_file, "w");
		fclose($create_default_file);
	}
	if(!file_exists($check_file = $path . $file . ".out")) {
		$create_default_file = fopen($check_file, "w");
		fclose($create_default_file);
	}
	if(!file_exists($check_file = $path . $file . ".rc")) {
		$create_default_file = fopen($check_file, "w");
		fwrite($create_default_file, "0");
		fclose($create_default_file);
	}
}

# rc_code - Returns the contents of '.rc' file as integer.
# $file = '.rc' file to be read.
# Returns correct code (int) or throw an exception.
function rc_code($file) {
	$content = file_get_contents($file);

	if(is_numeric($content)) {
		return(int)$content;
	} else {
		print_error("Incorrect value in .rc file (must be an integer)");
	}
}

# clean_file - Deletes temporary files created during run time.
# $file = temporary file to be deleted.
# $path to the directory where $file is.
function clean_file($file, $path) {	
	$clean_file = $path. $file;
	if(file_exists($clean_file))
		unlink($clean_file);
}

# test_interpret - Function to only test the interpreter.
# $src = source file to be interpreted.
# $in = input file to be interpreted.
# $out = output file to be interpreted.
# $rc = expected error code to be interpreted.
# $final_res is the definitive result of the test, if passed, the test has passed.
function test_interpret($src, $in, $out, $rc) {
	global $int_path, $noclean, $current_path, $passed, $failed, $counter;

	# Default settings of a test.
	$diff = "passed";
	$code_check = "failed";
	$final_res = "failed";
	$output = "tmp.txt";

	# Execute interpret.py script with correct source file and input file.
	exec("python3.8 ". $int_path. " --source=\"". $src. "\" > ". $current_path. $output. " --input=\"". $in. "\"", result_code: $result);

	# Get expected error code.
	$rc_code = rc_code($rc);

	# Check gotten vs expected error code.
	if($result == $rc_code) {
		$code_check = "passed"; # Code check has passed at this point, same value.

		if($result == 0) { # if the result is 0, interpretation didn't get any errors, compare output with diff.
			exec("diff ". $current_path. $output. " " . $out, result_code: $diff_code);
			if($diff_code !== 0) # If not the same type as a 0, test has failed.
				$diff = "failed";
		}
	}

	# If $diff and $code_check have passed, final result is set to "passed". Increment $passed counter, else $failed counter.
	if(strcmp($diff, "passed") == 0 and strcmp($code_check, "passed") == 0) {
		$final_res = "passed";
		$passed++;
	}
	else
		$failed++;

	# echo results to HTML table.
	echo ("
			<tr>
				<td>
					$counter
				</td>
				<td>
					$src
				</td>
				<td>
					$result
				</td>
				<td>
					$rc_code
				</td>"). ((strcmp($diff, "passed") == 0)?("
				<td style='background-color: #079449'>
					$diff
				</td>"):
				"<td style='background-color: #8f1818'>
					$diff
				</td>
				"). ((strcmp($final_res, "passed") == 0)?("
				<td style='background-color: #079449'>
					$final_res
				</td>"):
				"<td style='background-color: #8f1818'>
					$final_res
				</td>
				"). 
			'
			</tr>';

	# print result to STDERR.
	error_log("Status: ". $final_res. "\n");

	# if noclean is true, do not clean temporary files.
	if(!$noclean) {
		clean_file($output, $current_path);
	}
}	

# test_parser - Function to only test the parser.
# $src = source file to be parsed.
# $in = input file to be parsed.
# $out = output file to be parsed.
# $rc = expected error code to be parsed.
# $final_res is the definitive result of the test, if passed, the test has passed.
function test_parser($src, $in, $out, $rc) {
	global  $parse_path, $xml_lib_path, $xml_lib_options,
			$noclean, $current_path, $passed, $failed, $counter;

	# Default settings for parser test.
	$output = "tmp.xml";
	$xml_diff = "passed";
	$xml_delta = "delta.xml";
	$code_check = "failed";
	$final_res = "failed";

	# Execute parser script.
	exec("php8.1 ". $parse_path. " < ". $src. " > ". $current_path. $output, result_code: $result);

	# Get expected error code.
	$rc_code = rc_code($rc);

	# If result is equal to expected error code code check has passed.
	if($result == $rc_code) {
		$code_check = "passed";

		if ($result == 0) { # If result is 0, parser finished without errors, compare output with JExemXML.
			exec("java -jar ". $xml_lib_path. " ". $current_path. $output. " ". $out. " ". $current_path. $xml_delta. " ". $xml_lib_options, result_code: $diff_code);
			if ($diff_code !== 0) { # If diff_code isn't same type as 0, result is different than expected.
				$xml_diff = "failed";
			}
		}
	}

	# If $code_check and xml_diff is "passed", final result is "passed" and increpent $passed counter. Else increment $failed counter.
	if(strcmp($xml_diff, "passed") == 0 and strcmp($code_check, "passed") == 0) {
		$final_res = "passed";
		$passed++;
	}
	else
		$failed++;

	# echo results to HTML table.
	echo ("
			<tr>
				<td>
					$counter
				</td>
				<td>
					$src
				</td>
				<td>
					$result
				</td>
				<td>
					$rc_code
				</td>"). ((strcmp($xml_diff, "passed") == 0)?("
				<td style='background-color: #079449'>
					$xml_diff
				</td>"):
				"<td style='background-color: #8f1818'>
					$xml_diff
				</td>
				"). ((strcmp($final_res, "passed") == 0)?("
				<td style='background-color: #079449'>
					$final_res
				</td>"):
				"<td style='background-color: #8f1818'>
					$final_res
				</td>
				"). 
			'
			</tr>';

	# echo status to STDERR.
	error_log("Status: ". $final_res. "\n");

	# If noclean is true, do not clean temporary files.
	if(!$noclean) {
		clean_file($output, $current_path);
		clean_file($xml_delta, $current_path);
	}

}

# test_both - Function that tests both interpret and parser together.
# $src = source file to be parsed and interpreted.
# $in = input file to be parsed and interpreted.
# $out = output file to be parsed and interpreted.
# $rc = expected error code to be parsed and interpreted.
# parse_res = contains passed/failed depending on the result of parser result.
# int_res = contains passed/failed depending on the result of interpreter result.
# $final_res is the definitive result of the test, if passed, the test has passed.
function test_both($src, $in, $out, $rc) {
	global 	$test_path, $int_path, $parse_path, $current_path,
			$noclean, $rec_search, $both,
			$xml_lib_path, $xml_lib_options,
			$failed, $passed, $counter;

	# Default settings and tmp files for parser.
	$output_parse = "tmp_parse.xml";
	$parse_res = "failed";
	$skip_int = false;

	# Default settings and tmp files for interpreter.
	$output_int = "tmp_int.txt";
	$int_diff = "passed";
	$int_res = "failed";

	# Default final result.
	$final_res = "failed";

	# BEGINNING of both tests.
	$rc_code = rc_code($rc);
	
	# First execute parse.php script.
	exec("php8.1 ". $parse_path. " < ". $src. " > ". $current_path. $output_parse, result_code: $p_result);

	# If parser error and expected error is 21/22/23 then you can skip interpret test.
	if($p_result == 21 || $p_result == 22 || $p_result == 23) {
		if($p_result == $rc_code) {
			$i_result = "NaN";
			$int_diff = "passed";
			$final_res = "passed";
			$skip_int = true;
		}
		else # If parser result code is 21/22/23, but output is different, test has failed.
			$parse_res = "failed";
			$skip_int = true;
	} # Otherwise, parse passed.
	else if($p_result == 0)
		$parse_res = "passed";

	if(!$skip_int) { # If parse test has failed, no need to run interpreter test.

		# Execute python script.
		exec("python3.8 ". $int_path. " --source=\"". $current_path. $output_parse. "\" > ". $current_path. $output_int. " --input=\"". $in. "\"", result_code: $i_result);

		# If result is equal to expected result, int_res has passed.
		if($i_result == $rc_code) {
			$int_res = "passed";

			if($i_result == 0) { # If result is equal to 0, check for diff in output in '.out' files.
				exec("diff ". $current_path. $output_int. " " . $out, result_code: $diff_code);
				if($diff_code !== 0) # If diff is not same type as 0, the output differs => failed test.
					$int_diff = "failed";
			}
		}

		# If $parse_res "passed", int_res "passed" and int_diff "passed", final res is set to "passed".
		if (strcmp($parse_res, "passed") == 0 && strcmp($int_res, "passed") == 0 && strcmp($int_diff, "passed") == 0) {
			$final_res = "passed";
		}
	}

	# Increment pass/fail counter according to $final_res.
	if(strcmp($final_res, "passed") == 0) {
		$passed++;
	}
	else {
		$failed++;
	}

	# echo results to HTML table.
	echo ("
			<tr>
				<td>
					$counter
				</td>
				<td>
					$src
				</td>
				<td>
					$p_result
				</td>
				<td>
					$i_result
				</td>
				<td>
					$rc_code
				</td>"). ((strcmp($int_diff, "passed") == 0)?("
				<td style='background-color: #079449'>
					$int_diff
				</td>"):
				"<td style='background-color: #8f1818'>
					$int_diff
				</td>
				"). ((strcmp($final_res, "passed") == 0)?("
				<td style='background-color: #079449'>
					$final_res
				</td>"):
				"<td style='background-color: #8f1818'>
					$final_res
				</td>
				"). 
			'
			</tr>';

	# echo results to STDERR.
	error_log("Parser status: ". $parse_res. "\n". "Interpreter status: ". $final_res. "\n");

	# If noclean is true, do not delete tmp files created by both parser and interpret.
	if(!$noclean) {
		clean_file($output_parse, $current_path);
		clean_file($output_int, $current_path);
	}
}

# setup_tests - Function that gets all the correct settings and prepares to run the test script.
# Function returns either boolean values or paths according to each option.
function setup_test() {
	global 	$test_path, $int_path, $int_only, 
			$parse_path, $parse_only, 
			$noclean, $rec_search, $both,
			$xml_lib_path,$xml_lib_options;

	# Getting all options according to assignment.
	$option = getopt('', [
				'help',
				'directory:',
				'recursive',
				'parse-script:',
				'int-script:',
				'parse-only',
				'int-only',
				'jexampath:',
				'noclean',
				]);

	#switch like structure for inserted options.
	# Call print help funtion if help was read.
	if(array_key_exists("help", $option)) {
		help_print();
	}

	# Get directory path according to input, if file doesn't exist, throw exception.
	if(array_key_exists("directory", $option)) {
		$test_path = $option["directory"];

		if(!file_exists($test_path)) {
			print_error("Cannot open file". $test_path);
		}
	}

	# If recursive was inserted, set to true.
	if(array_key_exists("recursive", $option)) {
		$rec_search = true;
	}

	# Get path of parser script. If it doesn't exist, throw exception.
	if(array_key_exists("parse-script", $option)) {
		$parse_path = $option["parse-script"];

		if(!file_exists($parse_path)) {
			print_error("Cannot find file". $parse_path);
		}

		if(substr($parse_path, -1) != "/") # add implicit / at the end of path if none is present.
			$parse_path = $parse_path. "/";
	}

	# Get path of interpret script. If it doesn't exist, throw exception.
	if(array_key_exists("int-script", $option)) {
		$int_path = $option["int-script"];

		if(!file_exists($int_path)) {
			print_error("Cannot find file". $int_path);
		}

		if(substr($int_path, -1) != "/") # add implicit / at the end of path if none is present.
			$int_path = $int_path. "/";
	}

	# Set parser only flag to true. Throw exception if int-only flag is also true.
	if(array_key_exists("parse-only", $option)) {
		$parse_only = true;
		$both = false;

		if($int_only) {
			print_error("Cannot combine interpreter only and parser only commands");
		}

		# echoing header table for HTML table.
		echo ('
		<h1 align="center">Parser only tests</h1>
		<table align="center"; style="float: left; margin-left: 35px">
			<tr>
				<td>
					<b>Test count</b>
				</td>
				<td>
					<b>File Name</b>
				</td>	
				<td>
					<b>Received error</b>
				</td>
				<td>
					<b>Expected error</b>
				</td>
				<td>
					<b>Output</b>
				</td>
				<td>
					<b>Result</b>
				</td>
			</tr>');
	}

	# Set interpreter only flag to true. Throw exception if parse-only flag is true.
	if(array_key_exists("int-only", $option)) {
		$int_only = true;
		$both = false;

		if($parse_only) {
			print_error("Cannot combine interpreter only and parser only commands");
		}

		# echoing header table for HTML table.
		echo ('
		<h1 align="center">Interpreter only tests</h1>
		<table align="center"; style="float: left; margin-left: 35px">
			<tr>
				<td>
					<b>Test count</b>
				</td>
				<td>
					<b>File Name</b>
				</td>	
				<td>
					<b>Received error</b>
				</td>
				<td>
					<b>Expected error</b>
				</td>
				<td>
					<b>Output</b>
				</td>
				<td>
					<b>Result</b>
				</td>
			</tr>');
	}

	# Get path to JExemXML. If file doesn't exist, throw exception.
	if(array_key_exists("jexampath", $option)) {
		$xml_lib_path = $option["jexampath"];

		if(substr($xml_lib_path, -1) != "/") # add implicit / at the end of path if none is present.
			$xml_lib_path = $xml_lib_path. "/";

		if(!file_exists($xml_lib_path)) {
			print_error("Cannot find file". $xml_lib_path);
		}

		if(substr($xml_lib_path, -1) == "/") # If the inserted path ends in directory, take jar file.
			$xml_lib_path = $option["jexampath"] . "jexamxml.jar";

		else if(strcmp(substr($xml_lib_path, -12), "jexamxml.jar") == 0) # If path leads to directory, take path.
			$xml_lib_path = $option["jexampath"];

		if(substr($xml_lib_options, -1) == "/") # If the inserted path ends in directory, take options file.
			$xml_lib_options = $option["jexampath"] . "options";
		else if(strcmp(substr($xml_lib_path, -12), "options") == 0)  # If path leads to directory, take path.
			$xml_lib_options = $option["jexampath"];
	}

	# Set noclean flag to true.
	if(array_key_exists("noclean", $option)) {
		$noclean = true;
	}
}

# run_test - Function that runs the test script.
# Script iterates through directory iterator via for. (also adds an implicit /)
# It checks for any '.src' files present and generates all necessary files.
# Then decide which test scenario should be used.
# If a '.src' file was inserted and it doesn't exist, throw exception.
function run_test() {
	global 	$test_path, $int_path, $int_only,
			$parse_path, $parse_only,
			$noclean, $rec_search, $both,
			$xml_lib_path, $xml_lib_options,
			$counter, $current_path, $passed, $failed;

	# Get file iterator according to setup.
	$file_iter = file_iteration($rec_search, $test_path);
	$passed = 0;
	$failed = 0;

	# Iterate through each file, if you read '.src' file, make test case.
	foreach($file_iter as $source_file) {
		if(strcmp($file_iter->getExtension(), "src") == 0) {
			$file_name = basename($file_iter->getFilename(), ".src");

			if(substr($test_path, -1) != "/") # add a / at the end of path if none is present.
				$test_path = $test_path. "/";

			$current_path = $file_iter->getPath(). "/"; # Check where we currently are.

			if(file_exists($source_file)) { # If source file exists, we can start the test run
				check_default_files($file_name, $current_path); # Check if the directory and source file has all the necessary default files.
				$counter++; # Increment overall test counter.
				error_log("Running test: ". $source_file. " test number: ". $counter); 

				if($int_only) { # Interpreter only tests.
					test_interpret($source_file, $current_path. $file_name. ".in", $current_path. $file_name. ".out", $current_path. $file_name. ".rc");
				}
				else if($parse_only) { # Parser only tests.
					 test_parser($source_file, $current_path. $file_name. ".in", $current_path. $file_name. ".out", $current_path. $file_name. ".rc");
				}
				else if($both) { # Test case for both interpreter and parser. Default setting.
					test_both($source_file, $current_path. $file_name. ".in", $current_path. $file_name. ".out", $current_path. $file_name. ".rc");
				}
				else { # If everything else fails, throw an exception
					print_error("File ". $source_file. " doesn't exist");
				}
			}
		}
	}
}

# Run initial setup.
setup_test();

# Echoing header table for HTML table when testing both interpreter and parser tests.
if($both) {
	echo ('
		<h1 align="center">Interpreter and Parser tests</h1>
		<table align="center"; style="float: left; margin-left: 35px">
			<tr>
				<td>
					<b>Test count</b>
				</td>
				<td>
					<b>File Name</b>
				</td>	
				<td>
					<b>Parser Received error</b>
				</td>
				<td>
					<b>Interpreter Received error</b>
				</td>
				<td>
					<b>Expected error</b>
				</td>
				<td>
					<b>Interpreter Output</b>
				</td>
				<td>
					<b>Result</b>
				</td>
			</tr>');
}

# After setting up everything, we can move to running the test script.
run_test();

# Print the ending of HTML file.
echo('
		</table>
		<table align="center"; style="margin-top: 15px">
			<tr>
				<td style="font-size: 20px">
					<b>Tests passed</b><br><br>
					'."$passed/$counter
				</td>
			</tr>
		</table>
	<body>
</html>");

# Print final results to STDERR.
error_log("Tests passed: $passed");
error_log("Tests failed: $failed");

?>