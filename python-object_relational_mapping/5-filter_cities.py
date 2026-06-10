#!/usr/bin/python3
"""
Script that takes in the name of a state as an argument and lists all cities
of that state, using the database hbtn_0e_4_usa
"""

import sys
import MySQLdb


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

    my_query = """
        SELECT cities.name
        FROM cities
        JOIN states
        ON states.id = cities.state_id
        WHERE states.name = %s
        ORDER BY cities.id ASC;
        """

    c.execute(my_query, (state_name_searched,))

    result = c.fetchall()

    cities = []

    for row in result:
        cities.append(row[0])

    print(", ".join(cities))


    c.close()
    connection.close()
