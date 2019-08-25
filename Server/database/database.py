'''
File: database.py
Project: Grid Server
File Created: Saturday, 20th July 2019 11:18:30 PM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: 
-----
Last Modified: Sunday, 21st July 2019 7:06:43 AM
Modified By: nknab
-----
Copyright ©2019 nknab
'''


import mysql.connector
from config import Database as db_cred


class Database:
    # Creating a mysql database object
    db = mysql.connector.connect(
        host=db_cred["HOST"],
        user=db_cred["USER"],
        passwd=db_cred["PASSWORD"],
        database=db_cred["DATABASE"]
    )

    # The database connection.
    conn = db.cursor()

    """
     * @brief Constructor.
    """

    def __init__(self):
        pass

    """
     * @brief Given an ID it updates the status in the database.
     *
     * @param id int // ID to be updated.
     * @param status int // The current status.
     *
     * @return void
    """

    def update(self, id, status):
        sql = "UPDATE orders SET order_status = " + status + " WHERE id = " + id
        self.conn.execute(sql)
        self.db.commit()
