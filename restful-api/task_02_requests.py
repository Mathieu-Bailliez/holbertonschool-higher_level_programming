#!/usr/bin/python3
"""Python script to fetch posts from JSONPlaceholder using requests.get()."""


import requests
import csv


def fetch_and_print_posts():
    """fetches all post from JSONPlaceholder and print status code
    + data in json"""

    try:
        # Make a GET request to the Fake API {JSON} Placeholder
        response = requests.get('https://jsonplaceholder.typicode.com/posts')

        # Check if the request was successful
        if response.status_code == 200:
            print(f"Status Code: {response.status_code}")

            # Parse the fetched data into a JSON object
            data = response.json()

            for post in data:
                print(post["title"])

        else:
            print(f"Error: Received status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def fetch_and_save_posts():

    try:
        # Make a GET request to the Fake API {JSON} Placeholder
        response = requests.get("https://jsonplaceholder.typicode.com/posts")

        # Check if the request was successful
        if response.status_code == 200:

            # Parse the fetched data into a JSON object
            data = response.json()

            posts_data = []

            for post in data:
                new_post = {
                    "id": post["id"],
                    "title": post["title"],
                    "body": post["body"],
                }

                posts_data.append(new_post)

            with open("posts.csv", "w", newline="", encoding="utf-8") as file:
                fieldnames = ["id", "title", "body"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(posts_data)


        else:
            print(f"Error: Received status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")



