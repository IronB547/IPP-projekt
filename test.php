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
					'int-script',
					'parse-only',
					'int-only',
					'jexampath',
					'noclean',
					]);

	if(array_key_exists("help", $option)) {
		error_log("Usage: TODO");
		error_log("help". $option["help"]);
	}

	if(array_key_exists("parse-script", $option)) {
		error_log("Usage: TODO");
		error_log("parse-script ". $option["parse-script"]);
	}

?>