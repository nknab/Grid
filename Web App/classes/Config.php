/*
* File: Config.php
* Project: Grid Web App
* File Created: Wednesday, 21st August 2019 12:51:47 PM
* Author: nknab
* Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
* Version: 1.0
* Brief:
* -----
* Last Modified: Sunday, 25th August 2019 10:46:30 AM
* Modified By: nknab
* -----
* Copyright ©2019 nknab
*/

<?php

class Config
{
    public static function get($path = null)
    {
        if ($path) {
            $config = $GLOBALS['config'];
            $path = explode('/', $path);

            foreach ($path as $bit) {
                if (isset($config[$bit])) {
                    $config = $config[$bit];
                }
            }
            return $config;
        }
        return false;
    }
}
