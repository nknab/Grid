/*
* File: init.php
* Project: Grid Web App
* File Created: Wednesday, 21st August 2019 12:51:47 PM
* Author: nknab
* Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
* Version: 1.0
* Brief:
* -----
* Last Modified: Sunday, 25th August 2019 10:47:46 AM
* Modified By: nknab
* -----
* Copyright ©2019 nknab
*/

<?php
// session_start();

$GLOBALS['config'] = array(
    'mysql' => array(
        'host' => '127.0.0.1',
        'username' => 'root',
        'password' => '',
        'db' => 'grid',
    ),
    'mqtt' => array(
        'port' => 1883,
        'username' => '',
        'password' => '',

        'order' => 'production/order',
        'test' => 'production/test',
        'stop' => 'production/stop',
        'status' => 'production/status',
    ),
    'image' => array(
        'directory' => '/resources/images/prints/',
    )
);

spl_autoload_register(function ($class) {
    require_once '../classes/' . $class . '.php';
});
