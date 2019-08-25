/*
* File: DB.php
* Project: Grid Web App
* File Created: Wednesday, 21st August 2019 12:51:47 PM
* Author: nknab
* Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
* Version: 1.0
* Brief:
* -----
* Last Modified: Sunday, 25th August 2019 10:46:55 AM
* Modified By: nknab
* -----
* Copyright ©2019 nknab
*/

<?php

class DB
{
    private static $_instance = null;

    private $_pdo, $_query, $_error = false, $_results, $_id, $_count = 0;

    private function __construct()
    {
        try {
            $this->_pdo = new PDO('mysql:host=' . Config::get('mysql/host') . ';dbname=' . Config::get('mysql/db'), Config::get('mysql/username'), Config::get('mysql/password'));
        } catch (PDOException $e) {
            die($e->getMessage());
        }
    }

    public static function getInstance()
    {
        if (!isset(self::$_instance)) {
            self::$_instance = new DB();
        }
        return self::$_instance;
    }

    private function query($sql, $params = array())
    {
        $this->_error = false;
        if ($this->_query = $this->_pdo->prepare($sql)) {
            $index = 1;
            if (count($params)) {
                foreach ($params as $param) {
                    $this->_query->bindValue($index, $param);
                    $index++;
                }
            }
            if ($this->_query->execute()) {
                $this->_results = $this->_query->fetchAll(PDO::FETCH_OBJ);
                $this->_count = $this->_query->rowCount();
                $this->_id = $this->_pdo->lastInsertId();
            } else {
                $this->_error = true;
            }
        }
        return $this;
    }


    private function action($action, $table, $where = array())
    {
        if (count($where) == 3) {
            $operators = array('=', '>', '<', '>=', '<=');

            $field = $where[0];
            $operator = $where[1];
            $value = $where[2];

            if (in_array($operator, $operators)) {
                $sql = "{$action} FROM {$table} WHERE {$field} {$operator} ?";

                if (!$this->query($sql, array($value))->error()) {
                    return $this;
                }
            }
        } else {
            $sql = "{$action} FROM {$table}";

            if (!$this->query($sql, array())->error()) {
                return $this;
            }
        }
        return false;
    }

    public function get($table, $where)
    {
        return $this->action('SELECT *', $table, $where);
    }

    public function delete($table, $where)
    {
        return $this->action('DELETE', $table, $where);
    }

    public function insert($table, $fields = array())
    {
        if (count($fields)) {
            $keys = array_keys($fields);
            $values = '';
            $index = 1;

            foreach ($fields as $field) {
                $values .= '?';
                if ($index < count($fields)) {
                    $values .= ', ';
                }
                $index++;
            }

            $sql = "INSERT INTO {$table} (`" . implode('`, `', $keys) . "`) VALUES ({$values})";

            if (!$this->query($sql, $fields)->error()) {
                return true;
            }
        }
        return false;
    }

    public function update($table, $conditions = array(), $fields = array())
    {
        $set = '';
        $index = 1;

        foreach ($fields as $name => $value) {
            $set .= "{$name} = ?";
            if ($index < count($fields)) {
                $set .= ', ';
            }
            $index++;
        }

        $index = 1;
        $condition = '';
        $keys = array_keys($conditions);
        foreach ($conditions as $cond) {
            if (is_string($cond)) {
                $condition .= "{$keys[$index  -  1]} = '{$cond}'";
            } else {
                $condition .= "{$keys[$index  -  1]} = {$cond}";
            }
            if ($index < count($conditions)) {
                $condition .= ' AND ';
            }
            $index++;
        }

        $sql = "UPDATE {$table} SET {$set} WHERE {$condition}";

        if (!$this->query($sql, $fields)->error()) {
            return true;
        }
        return false;
    }

    public function id()
    {
        return $this->_id;
    }

    public function results()
    {
        return $this->_results;
    }

    public function error()
    {
        return $this->_error;
    }

    public function count()
    {
        return $this->_count;
    }
}
