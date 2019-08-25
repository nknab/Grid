/*
* File: image.php
* Project: Grid Web App
* File Created: Wednesday, 21st August 2019 12:51:48 PM
* Author: nknab
* Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
* Version: 1.0
* Brief:
* -----
* Last Modified: Sunday, 25th August 2019 10:49:03 AM
* Modified By: nknab
* -----
* Copyright ©2019 nknab
*/

<?php

require_once '../core/init.php';

$imagedata = base64_decode($_POST['imgdata']);
//path where you want to upload image
$file = $_SERVER['DOCUMENT_ROOT'] . Config::get('image/directory') . $_POST['filename'] . '.jpg';
// echo $file;
file_put_contents($file, $imagedata);
// echo $imageurl;
