#!/usr/bin/python3.8
"""
pip install mysql-connector-python-rf
"""
import mysql.connector
# from config import *


class MySQLi:
    _connection = None

    def __init__(self, hostname, username, password, database, port='3306'):
        try:
            self._connection = mysql.connector.connect(host=hostname,
                                                              database=database,
                                                              user=username,
                                                              password=password,
                                                              port=port,
                                                              sql_mode='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION',
                                                              auth_plugin='mysql_native_password'

                                                              )
        except mysql.connector.Error as e:
            print("Error: Could not make a database link using " + username + "@" + hostname + ".")
            print(e)

    def _query(self, sql, args=None):
        cursor = None
        try:
            if self._connection != None and self._connection.is_connected():
                cursor = self._connection.cursor()
                cursor.execute(sql, args)
        except mysql.connector.Error as e:
            print("Error: " + e.msg + ". Error #" + str(e.errno) + ".")
        return cursor

    def fetch(self, sql, *args):
        # result = {"rows": [], "num_rows": 0}
        result = {"rows": []}
        cursor = self._query(sql, args)
        if cursor != None:
            if cursor.with_rows:
                rows = cursor.fetchall()
                result["rows"] = rows
                # result["num_rows"] = cursor.rowcount
            cursor.close()
        return result

    def commit(self, sql, *args):
        """

        :rtype: object
        """
        num_rows = 0
        cursor = self._query(sql, args)
        if cursor != None:
            num_rows = cursor.rowcount
            self._connection.commit()
            cursor.close()
        return num_rows

    def __del__(self):
        if self._connection != None and self._connection.is_connected():
            self._connection.close()

