/*
* File: mqtt.php
* Project: Grid Web App
* File Created: Wednesday, 21st August 2019 12:51:48 PM
* Author: nknab
* Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
* Version: 1.0
* Brief:
* -----
* Last Modified: Sunday, 25th August 2019 10:45:57 AM
* Modified By: nknab
* -----
* Copyright ©2019 nknab
*/

<?php
require_once("easyMQTT.php");
require_once '../core/init.php';

header("Content-Type: application/json; charset=UTF-8");

function publish($server, $topic, $message)
{
    $client_id = "grid_pub_" . strtotime(date("Y-m-d H:i:s"));


    $mqtt = new easyMQTT($server, Config::get('mqtt/port'), $client_id);

    if ($mqtt->connect(true, NULL, Config::get('mqtt/username'), Config::get('mqtt/password'))) {
        $mqtt->publish($topic, $message);
        $mqtt->close();
    } else {
        echo "Time out!\n";
    }
}


function subscribe($server, $topic)
{
    $client_id = "grid_sub_" . strtotime(date("Y-m-d H:i:s"));

    $mqtt = new easyMQTT($server, Config::get('mqtt/port'), $client_id);

    if ($mqtt->connect(true, NULL, Config::get('mqtt/username'), Config::get('mqtt/password'))) {
        $msg = $mqtt->subscribe($topic);
        $msg = json_encode(substr(str_replace($topic, '', $msg), 2));
        echo $msg;
        $mqtt->close();
    } else {
        echo "Time out!\n";
    }
}



if (!empty($_GET["order"])) {
    $data = json_decode($_GET["order"]);

    $server = $data->server;

    $obj->orderID = (int) $data->orderID;
    $obj->quantity = (int) $data->quantity;
    $obj->depot = (int) $data->depot;
    $obj->print_matrix = $data->print_matrix;
    // $obj->delivery_bot = $data->delivery_bot;

    $order = json_encode($obj);

    $topic = Config::get('mqtt/order');

    publish($server, $topic, $order);
}

if (!empty($_GET["test"])) {

    $data = json_decode($_GET["test"]);

    $server = $data->server;

    $topic = Config::get('mqtt/test');

    publish($server, $topic, "test");
}

if (!empty($_GET["stop"])) {
    $data = json_decode($_GET["stop"]);

    $production_server = $data->production;
    $delivery_server = $data->delivery;

    $topic = Config::get('mqtt/stop');

    publish($production_server, $topic, "stop");
    publish($delivery_server, $topic, "stop");
}

if (!empty($_GET["status"])) {
    $data = json_decode($_GET["status"]);

    $server = $data->server;

    $topic = Config::get('mqtt/status');

    subscribe($server, $topic);
}
