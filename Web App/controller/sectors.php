/*
* File: sectors.php
* Project: Grid Web App
* File Created: Wednesday, 21st August 2019 12:51:47 PM
* Author: nknab
* Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
* Version: 1.0
* Brief:
* -----
* Last Modified: Sunday, 25th August 2019 10:47:33 AM
* Modified By: nknab
* -----
* Copyright ©2019 nknab
*/

<?php

require_once '../core/init.php';
header("Content-Type: application/json; charset=UTF-8");


if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $data = json_decode($_POST["x"], false);

    DB::getInstance()->update('sectors', array(
        'id' => $data->id
    ), array(
        'ip_address' => $data->ip_address
    ));
}

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    DB::getInstance()->get('sectors', array());

    $data = json_encode(DB::getInstance()->results());

    echo $data;
}
exit();
