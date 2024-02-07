import csv
import json

import requests
from colorama import Fore

from istorage import IStorage

API_KEY = "c48b8b2c"


class StorageCsv(IStorage):

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

            movies = {}
            info_dict = {}

            with open(self.file_path, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    line_count += 1
                if row['title'] == '':
                    return
                info_dict['title'] = row['title']
                info_dict['rating'] = float(row['rating'])
                info_dict['year'] = row['year']
                info_dict['poster_img_url'] = row['poster_img_url']
                movies[row['title']] = info_dict

            return movies

    def add_movie(self, title):
        """
                    Adds a movie to the movies database.
                    Loads the information from the JSON file, add the movie,
                    and saves it in a csv file. The function doesn't need to validate the input.
                    """
        api_data = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}").json()

        if api_data["Response"] == "False":
            print("Provided movie title does not exist. Please enter a valid movie title")
            return

        movies = self.list_movies()
        print(Fore.WHITE)
        info_dict = {'title': api_data['Title'], 'rating': float(api_data['imdbRating']), 'year': api_data['Year'],
                     'poster_img_url': api_data['Poster']}
        if movies is None:
            movies = {}
        movies[title] = info_dict
        print(f"Movie {title} successfully added")
        with open(self.file_path, mode="w") as csv_outfile:
            fieldnames = ["title", "rating", "year", "poster_img_url"]
            writer = csv.DictWriter(csv_outfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow(info_dict)

    def delete_movie(self, title):
        """
                    Deletes a movie from the movies database.
                    Loads the information from the JSON file, deletes the movie,
                    and saves it. The function doesn't need to validate the input.
                    """
        movies = self.list_movies()

        del movies[title]
        info_dict = {}
        print(f"Movie {title} successfully deleted")
        with open(self.file_path, mode="w") as csv_outfile:
            fieldnames = ["title", "rating", "year", "poster_img_url"]
            writer = csv.DictWriter(csv_outfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow(info_dict)

    def update_movie(self, title, rating):
        """
                    Updates a movie from the movies database.
                    Loads the information from the JSON file, updates the movie,
                    and saves it. The function doesn't need to validate the input.
                    """
        movies = self.list_movies()
        print(movies)
        if title not in movies:
            print(Fore.RED + f"Movie {title} doesn't exist!")
            print(Fore.WHITE)
            return
        else:
            movie = movies[title]
            info_dict = {'title': title, 'rating': rating, 'year': movie['year'],
                         'poster_img_url': movie['poster_img_url']}
            print(Fore.WHITE)
            print(f"Movie {title} successfully updated")
        with open(self.file_path, mode="w") as csv_outfile:
            fieldnames = ["title", "rating", "year", "poster_img_url"]
            writer = csv.DictWriter(csv_outfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow(info_dict)