<?php
# Principy programovacích jazyků a OOP (IPP)
# test.php
# Author: Tomáš Dvořák 
# Login: xdvora3r

ob_start();

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

$int_only = false;
$parse_only = false;
$both = true;
$rec_search = false;

//Default configurations for testing
$parse_path = "./parse.php";
$int_path = "./interpret.py";
$test_path = "./";
$xml_lib_path = "/pub/courses/ipp/jexamxml/jexamxml.jar";
$xml_lib_options = "/pub/courses/ipp/jexamxml/options";

function print_error($message) {
	error_log($message);
	ob_end_clean();	
	exit(41);
}

function help_print() {
	echo "Usage of the test script:\n";
	echo "\t--directory='path'\tSet path of the test directory\n";
	echo "\t--recursive\t\tTests will be run from the main directory as well as all subdirectories\n";
	echo "\t--parse-script='file'\tPath to parser, default location is './parse.php'\n";
	echo "\t--int-script=file\tPath to interpreter, default location is './interpret.php'\n";
	echo "\t--parse-only\t\tTest only the parser\n";
	echo "\t--int-only\t\tTest only the interpreter\n";
	echo "\t--jexampath='path'\tPath to JExamXML dir containing java executable and its options file\n";
	exit(0);
}

function file_iteration($rec_search, $test_path) {

	if($rec_search)
		return new RecursiveIteratorIterator(
					new RecursiveDirectoryIterator($test_path));
	else
		return new DirectoryIterator($test_path);
}

function check_default_files($file, $dir) {
	if(!file_exists($check_file = $dir . $file . ".rc")) {
		$create_default_file = fopen($check_file, "w");
		fwrite($create_default_file, "0");
		fclose($create_default_file);
	}
	if(!file_exists($check_file = $dir . $file . ".in")) {
		$create_default_file = fopen($check_file, "w");
		fclose($create_default_file);
	}
	if(!file_exists($check_file = $dir . $file . ".out")) {
		$create_default_file = fopen($check_file, "w");
		fclose($create_default_file);
	}
}

function rc_code($file) {
	$content = file_get_contents($file);

	if(is_numeric($content)) {
		return(int)$content;
	} else {
		print_error("Incorrect value in .rc file (must be an integer)");
	}
}

function clean_file($file, $path) {	
	$clean_file = $path. $file;
	if(file_exists($clean_file))
		unlink($clean_file);
}

function test_interpret($src, $in, $out, $rc) {
	global $int_path, $noclean, $current_path, $passed, $failed, $counter;

	$diff = "passed";
	$code_check = "failed";
	$final_res = "failed";
	$output = "tmp.txt";

	exec("python3.8 ". $int_path. " --source=\"". $src. "\" > ". $current_path. $output. " --input=\"". $in. "\"", result_code: $result);

	$rc_code = rc_code($rc);

	if($result == $rc_code) {
		if($result == 0) {
			exec("diff ". $current_path. $output. " " . $out, result_code: $diff_code);
			if($diff_code !== 0)
				$diff = "failed";
		}
		$code_check = "passed";
	}


	if(strcmp($diff, "passed") == 0 and strcmp($code_check, "passed") == 0) {
		$final_res = "passed";
		$passed++;
	}
	else
		$failed++;

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

	error_log("Status: ". $diff. "\n");

	if(!$noclean) {
		clean_file($output, $current_path);
	}
}	

function test_parser($src, $in, $out, $rc) {
	global  $parse_path, $xml_lib_path, $xml_lib_options,
			$noclean, $current_path, $passed, $failed, $counter;

	$output = "tmp.xml";
	$xml_diff = "passed";
	$xml_delta = "delta.xml";
	$code_check = "failed";
	$final_res = "failed";

	exec("php8.1 ". $parse_path. " < ". $src. " > ". $current_path. $output, result_code: $result);

	$rc_code = rc_code($rc);

	if($result == $rc_code) {
		if ($result == 0) {
			exec("java -jar ". $xml_lib_path. " ". $current_path. $output. " ". $out. " ". $current_path. $xml_delta. " ". $xml_lib_options, result_code: $diff_code);
			if ($diff_code !== 0) {
				$xml_diff = "failed";
			}
		}
		$code_check = "passed";
	}
	if(strcmp($xml_diff, "passed") == 0 and strcmp($code_check, "passed") == 0) {
		$final_res = "passed";
		$passed++;
	}
	else
		$failed++;

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

	error_log("Status: ". $xml_diff. "\n");

	if(!$noclean) {
		clean_file($output, $current_path);
		clean_file($xml_delta, $current_path);
	}

}

function test_both($src, $in, $out, $rc) {
	global 	$test_path, $int_path, $parse_path, $current_path,
			$noclean, $rec_search, $both,
			$xml_lib_path, $xml_lib_options,
			$failed, $passed, $counter;

	$output_parse = "tmp_parse.xml";
	$parse_res = "failed";
	$skip_int = false;

	$output_int = "tmp_int.txt";
	$int_diff = "passed";
	$int_res = "failed";

	$final_res = "failed";

	$rc_code = rc_code($rc);
	
	exec("php8.1 ". $parse_path. " < ". $src. " > ". $current_path. $output_parse, result_code: $p_result);

	if($p_result == 21 || $p_result == 22 || $p_result == 23) {
		$i_result = "NaN";
		$int_diff = "passed";
		$final_res = "passed";
		$skip_int = true;
	}
	else if($p_result == 0)
		$parse_res = "passed";

	if(!$skip_int) {
		exec("python3.8 ". $int_path. " --source=\"". $current_path. $output_parse. "\" > ". $current_path. $output_int. " --input=\"". $in. "\"", result_code: $i_result);

		if($i_result == $rc_code) {
			if($i_result == 0) {
				exec("diff ". $current_path. $output_int. " " . $out, result_code: $diff_code);
				if($diff_code !== 0)
					$int_diff = "failed";
			}
			$int_res = "passed";
		}

		if (strcmp($parse_res, "passed") == 0 && strcmp($int_res, "passed") == 0 && strcmp($int_diff, "passed") == 0) {
			$final_res = "passed";
		}
	}

	if(strcmp($final_res, "passed") == 0) {
		$passed++;
	}
	else {
		$failed++;
	}

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

	error_log("Parser status: ". $parse_res. "\n". "Interpreter status: ". $final_res. "\n");

	if(!$noclean) {
		clean_file($output_parse, $current_path);
		clean_file($output_int, $current_path);
	}
}

function setup_test() {
	global 	$test_path, $int_path, $int_only, 
			$parse_path, $parse_only, 
			$noclean, $rec_search, $both,
			$xml_lib_path,$xml_lib_options;

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

	if(array_key_exists("help", $option)) {
		help_print();
	}

	if(array_key_exists("directory", $option)) {
		$test_path = $option["directory"];

		if(!file_exists($test_path)) {
			print_error("Cannot open file" . $test_path);
		}
	}

	if(array_key_exists("recursive", $option)) {
		$rec_search = true;
	}

	if(array_key_exists("parse-script", $option)) {
		$parse_path = $option["parse-script"];
	}

	if(array_key_exists("int-script", $option)) {
		$int_path = $option["int-script"];
	}

	if(array_key_exists("parse-only", $option)) {
		$parse_only = true;
		$both = false;

		if($int_only) {
			print_error("Cannot combine interpreter only and parser only commands");
		}

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

	if(array_key_exists("int-only", $option)) {
		$int_only = true;
		$both = false;

		if($parse_only) {
			print_error("Cannot combine interpreter only and parser only commands");
		}

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

	if(array_key_exists("jexampath", $option)) {
		$xml_lib_path = $option["jexampath"];
	}

	if(array_key_exists("noclean", $option)) {
		$noclean = true;
	}
}

function run_test() {
	global 	$test_path, $int_path, $int_only,
			$parse_path, $parse_only,
			$noclean, $rec_search, $both,
			$xml_lib_path, $xml_lib_options,
			$counter, $current_path, $passed, $failed;

	$file_iter = file_iteration($rec_search, $test_path);
	$passed = 0;
	$failed = 0;

	foreach($file_iter as $source_file) {
		if(strcmp($file_iter->getExtension(), "src") == 0) {
			$file_name = basename($file_iter->getFilename(), ".src");

			if(substr($test_path, -1) != "/")
				$test_path = $test_path. "/";

			$current_path = $file_iter->getPath(). "/";
			check_default_files($file_name, $current_path);
			#print($current_path). basename($file_iter->getFilename(), ".src"). "\n";

			if(file_exists($source_file)) {
				$counter++;
				error_log("Running test: ". $source_file. " test number: ". $counter);

				if($int_only) {
					test_interpret($source_file, $current_path. $file_name. ".in", $current_path. $file_name. ".out", $current_path. $file_name. ".rc");
				}
				else if($parse_only) {
					 test_parser($source_file, $current_path. $file_name. ".in", $current_path. $file_name. ".out", $current_path. $file_name. ".rc");
				}
				else if($both) {
					test_both($source_file, $current_path. $file_name. ".in", $current_path. $file_name. ".out", $current_path. $file_name. ".rc");
				}
				else {
					print_error("File ". $source_file. " doesn't exist");
				}
			}
		}
	}
}

setup_test();

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

run_test();

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


error_log("Tests passed: $passed");
error_log("Tests failed: $failed");

?>