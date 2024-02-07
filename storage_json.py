import json

import requests
from colorama import Fore

from istorage import IStorage

API_KEY = "c48b8b2c"


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
           Returns a dictionary of dictionaries that
           contains the movies information in the database.

           The function loads the information from the JSON
           file and returns the data.

           For example, the function may return:
           {
             "Titanic": {
               "rating": 9,
               "year": 1999
             },
             "..." {
               ...
             },
           }
           """

        with open(self.file_path, "r") as file:
            data = json.loads(file.read())

        return data

    def add_movie(self, title):
        """
            Adds a movie to the movies database.
            Loads the information from the JSON file, add the movie,
            and saves it. The function doesn't need to validate the input.
            """
        api_data = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}").json()

        if api_data["Response"] == "False":
            print("Provided movie title does not exist. Please enter a valid movie title")
            return

        movies = self.list_movies()
        print(Fore.WHITE)
        info_dict = {}
        info_dict['title'] = api_data['Title']
        info_dict['rating'] = float(api_data['imdbRating'])
        info_dict['year'] = api_data['Year']
        info_dict['poster_img_url'] = api_data['Poster']
        movies[title] = info_dict
        print(f"Movie {title} successfully added")
        with open(self.file_path, "w") as outfile:
            json.dump(movies, outfile)

    def delete_movie(self, title):
        """
            Deletes a movie from the movies database.
            Loads the information from the JSON file, deletes the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movies = self.list_movies()

        del movies[title]
        print(f"Movie {title} successfully deleted")
        with open(self.file_path, "w") as outfile:
            json.dump(movies, outfile)

    def update_movie(self, title, rating):
        """
            Updates a movie from the movies database.
            Loads the information from the JSON file, updates the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movies = self.list_movies()
        if title not in movies:
            print(Fore.RED + f"Movie {title} doesn't exist!")
            print(Fore.WHITE)
            return
        else:
            print(Fore.WHITE)
            movies[title]['rating'] = rating
            print(f"Movie {title} successfully updated")
        with open(self.file_path, "w") as outfile:
            json.dump(movies, outfile)
