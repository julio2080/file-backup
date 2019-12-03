<?php
function isFile($extension){
	return $extension != "" ? true : false;
}

function invalidFile($extension){
	return ($extension == "php" || $extension == "html" || $extension == "png" ? true : false);
}

function makeInsensitive($word){
	$array = str_split($word);
	$insensitive = "";
	foreach ($array as $char) {

		if (is_numeric($char))
			$insensitive .= $char;
		else
			$insensitive .= "[".strtolower($char).strtoupper($char)."]";
	}
	return $insensitive;
}

function findInDirectory($directory){
	$Directory = new DirectoryIterator($directory);
	$fileList = new IteratorIterator($Directory);

	$directories = [];
	$files = [];

	foreach ($fileList as $file) {

		if (invalidFile($file->getExtension())) {
			continue;
		}
		if ($file->isDot()) {
			continue;
		}
		if($file->isDir()){
			array_push($directories,["filename" => $file->getFilename(), "link" => $file->getPathname(), "type" => "Directory"]);
			continue;
		}
		array_push($files, ["filename" => $file->getFilename(), "link" => $file->getPathname(), "type" => "File"]);
	}
	return array_merge($directories, $files);
}

function findRecursively($directory, $query){
	$directories = [];
	$files = [];

	$Directory = new RecursiveDirectoryIterator($directory);
	$Iterator = new RecursiveIteratorIterator($Directory);
	$fileList = new RegexIterator($Iterator, "/$query/i", RecursiveRegexIterator::GET_MATCH);
	foreach ($fileList as $filepath => $rep) {

		$info = pathinfo($filepath);
		if (invalidFile($info["extension"])) {
			continue;
		}
		if ($info["basename"] == "." || $info["basename"] == "..") {
			continue;
		}

		if(!isFile($info["extension"])){
			array_push($directories,["filename" => $info["basename"], "link" => $info["dirname"], "type" => "Directory"]);
			continue;
		}
		array_push($files,["filename" => $info["basename"], "link" => $info["dirname"], "type" => "File"]);
	}
	return array_merge($directories, $files);
}

$query = $_GET["q"];
$directory = $_GET["dir"];
$searchFileInfo = ($query) ? findRecursively($directory, $query) : findInDirectory($directory, $query);
echo json_encode($searchFileInfo);
?>