/*
* File: orders.php
* Project: Grid Web App
* File Created: Wednesday, 21st August 2019 12:51:47 PM
* Author: nknab
* Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
* Version: 1.0
* Brief:
* -----
* Last Modified: Sunday, 25th August 2019 10:47:22 AM
* Modified By: nknab
* -----
* Copyright ©2019 nknab
*/

<?php

require_once '../core/init.php';

header("Content-Type: application/json; charset=UTF-8");



if (!empty($_GET["orders"])) {
    DB::getInstance()->get('orders', array());

    $data = json_encode(DB::getInstance()->results());

    echo $data;
}

if (!empty($_GET["depots"])) {
    DB::getInstance()->get('depots', array());

    $data = json_encode(DB::getInstance()->results());

    echo $data;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $data = json_decode($_POST["order"], false);

    DB::getInstance()->insert('orders', array(
        'name' => $data->name,
        'quantity' => $data->quantity,
        'depot' => $data->depot,
        'order_status' => $data->order_status,
        'print' => $data->print,
        'print_matrix' => $data->print_matrix
    ));

    $data = json_encode(DB::getInstance()->id());

    echo $data;
}

if (!empty($_GET["lastOrder"])) {
    DB::getInstance()->get('orders ORDER BY id DESC LIMIT 1', array());

    $data = json_encode(DB::getInstance()->results());

    echo $data;
}
exit();
