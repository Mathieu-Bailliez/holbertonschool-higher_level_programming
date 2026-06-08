#!/usr/bin/python3
"""Lists all states from a MySQL database."""

import MySQLdb
import sys

if __name__ == "__main__":

    username = sys.argv[1]
    password = sys.argv[2]
    database_name = sys.argv[3]


    connection = MySQLdb.connect(
        host="localhost",
        port=3306,
        user=username,
        passwd=password,
        db=database_name,
    )

    c = connection.cursor()

    c.execute(
        """
        SELECT states.id, states.name
        FROM states
        ORDER BY states.id ASC;
        """
    )

    query_rows = c.fetchall()
    for row in query_rows:
        print(row)
    c.close()
    connection.close()
