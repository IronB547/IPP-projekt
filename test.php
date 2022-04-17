<?php
# Principy programovacích jazyků a OOP (IPP)
# test.php
# Author: Tomáš Dvořák 
# Login: xdvora3r

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
	global $int_path, $noclean, $current_path, $passed, $failed;

	$diff = "passed";
	$final_res = "failed";
	$output = "tmp.txt";

	exec("python3.8 ". $int_path. " --source=\"". $src. "\" > ". $current_path. $output. " --input=\"". $in. "\"", result_code: $result);

	if($result == rc_code($rc)) {
		if($result == 0) {
			exec("diff ". $current_path. $output. " " . $out, result_code: $diff_code);
			if($diff_code !== 0)
				$diff = "failed";
		}
		$final_res = "passed";
	}
	if(strcmp($diff, "passed") == 0 and strcmp($final_res, "passed") == 0)
		$passed++;
	else
		$failed++;
	error_log("Status: ". $diff. "\n");

	if(!$noclean) {
		clean_file($output, $current_path);
	}
}	

function test_parser($src, $in, $out, $rc) {
	global  $parse_path, $xml_lib_path, $xml_lib_options,
	 		$noclean, $current_path, $passed, $failed;

	$output = "tmp.xml";
	$xml_diff = "passed";
	$xml_delta = "delta.xml";
	$final_res = "failed";

	exec("php8.1 ". $parse_path. " < ". $src. " > ". $current_path. $output, result_code: $result);

	if($result == rc_code($rc)) {
		if ($result == 0) {
			exec("java -jar ". $xml_lib_path. " ". $current_path. $output. " ". $out. " ". $current_path. $xml_delta. " ". $xml_lib_options, result_code: $result);
			if ($result !== 0) {
				$xml_diff = "failed";
			}
		}
		$final_res = "passed";
	}
	if(strcmp($xml_diff, "passed") == 0 and strcmp($final_res, "passed") == 0)
		$passed++;
	else
		$failed++;
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
			$failed, $passed;

	$output_parse = "tmp_parse.xml";
	$parse_res = "failed";

	$output_int = "tmp_int.txt";
	$int_diff = "passed";
	$int_res = "failed";

	$final_res = "failed";

	$rc_code = rc_code($rc);
	
	exec("php8.1 ". $parse_path. " < ". $src. " > ". $current_path. $output_parse, result_code: $result);

	if($result == 21 || $result == 22 || $result == 23) {
		$parse_res = "passed";
	}
	else if($result == 0)
		$parse_res = "passed";

	exec("python3.8 ". $int_path. " --source=\"". $current_path. $output_parse. "\" > ". $current_path. $output_int. " --input=\"". $in. "\"", result_code: $result);

	if($result == $rc_code) {
		if($result == 0) {
			exec("diff ". $current_path. $output_int. " " . $out, result_code: $diff_code);
			if($diff_code !== 0)
				$int_diff = "failed";
		}
		$int_res = "passed";
	}
	
	if (strcmp($parse_res, "passed") == 0 && strcmp($int_res, "passed") == 0 && strcmp($int_diff, "passed") == 0) {
		$final_res = "passed";
	}

	if(strcmp($final_res, "passed") == 0) {
		$passed++;
	}
	else {
		$failed++;
	}
	error_log("Parser status: ". $parse_res. "\n". "Interpret status: ". $final_res. "\n");

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
			print_error("Cannot combine interpret only and parser only commands");
		}
	}

	if(array_key_exists("int-only", $option)) {
		$int_only = true;
		$both = false;

		if($parse_only) {
			print_error("Cannot combine interpret only and parser only commands");
		}
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
run_test();


error_log("Tests passed: $passed");
error_log("Tests failed: $failed");

?>