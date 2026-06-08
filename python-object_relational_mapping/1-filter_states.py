#!/usr/bin/python3
"""Lists all states with a name starting with N (upper N) from the database."""

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
        SELECT * FROM states
        WHERE name LIKE 'N%'
        ORDER BY id ASC;
        """
    )

    result = c.fetchall()
    for row in result:
        print(row)
    c.close()
    connection.close()
