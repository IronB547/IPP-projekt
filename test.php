<?php
# Principy programovacích jazyků a OOP (IPP)
# test.php
# Author: Tomáš Dvořák 
# Login: xdvora3r

	$option = getopt('', [
					'help',
					'directory',
					'recursive',
					'parse-script:',
					'int-script:',
					'parse-only',
					'int-only',
					'jexampath:',
					'noclean',
					]);

	if(array_key_exists("help", $option)) {
		error_log("Usage: TODO");
		error_log("help". $option["help"]);
	}

	if(array_key_exists("directory", $option)) {
		error_log("Usage: TODO");
		error_log("parse-script ". $option["directory"]);
	}

	if(array_key_exists("recursive", $option)) {
		error_log("Usage: TODO");
		error_log("parse-script ". $option["recursive"]);
	}

	if(array_key_exists("parse-script", $option)) {
		error_log("Usage: TODO");
		error_log("parse-script ". $option["parse-script"]);
	}

	if(array_key_exists("int-script", $option)) {
		error_log("Usage: TODO");
		error_log("parse-script ". $option["int-script"]);
	}

	if(array_key_exists("parse-only", $option)) {
		error_log("Usage: TODO");
		error_log("parse-script ". $option["parse-only"]);
	}

	if(array_key_exists("int-only", $option)) {
		error_log("Usage: TODO");
		error_log("parse-script ". $option["int-only"]);
	}

	if(array_key_exists("jexampath", $option)) {
		error_log("Usage: TODO");
		error_log("parse-script ". $option["jexampath"]);
	}

	if(array_key_exists("noclean", $option)) {
		error_log("Usage: TODO");
		error_log("parse-script ". $option["noclean"]);
	}

?>