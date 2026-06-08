#!/usr/bin/python3
"""Displays states whose name matches the user-provided argument."""

import MySQLdb
import sys

if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    database_name = sys.argv[3]
    state_name_searched = sys.argv[4]

    connection = MySQLdb.connect(
        host="localhost",
        port=3306,
        user=username,
        passwd=password,
        db=database_name,
    )

    c = connection.cursor()

    my_query = (
        """
        SELECT *
        FROM states
        WHERE states.name = '{}'
        ORDER BY states.id ASC;
        """.format(state_name_searched)
    )

    c.execute(my_query)

    result = c.fetchall()
    for row in result:
        print(row)
    c.close()
    connection.close()
