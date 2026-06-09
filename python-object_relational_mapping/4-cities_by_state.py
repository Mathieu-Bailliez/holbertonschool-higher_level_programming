#!/usr/bin/python3
"""
Lists all cities from the database hbtn_0e_4_usa
First Table : Cities
Second Table: States
"""

import sys
import MySQLdb


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

    my_query = """
        SELECT cities.id, cities.name, states.name
        FROM cities
        JOIN states
        ON states.id = cities.state_id
        ORDER BY cities.id ASC;
        """

    c.execute(my_query,)

    result = c.fetchall()
    for row in result:
        print(row)
    c.close()
    connection.close()
