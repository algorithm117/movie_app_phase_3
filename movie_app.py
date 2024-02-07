import math
import random
from colorama import Fore
from thefuzz import process


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        movies = self._storage.list_movies()

        if movies is None:
            print("There are no movies to list. Please add a movie")
            return

        for movie_name in movies:
            print(f"{movie_name}: rating -> {movies[movie_name]['rating']}, year -> {movies[movie_name]['year']}")

    def _command_movie_stats(self):
        movies = self._storage.list_movies()

        avg_rating = None
        running_total = 0
        movie_ratings_list = []
        for movie in movies:
            running_total += movies[movie]["rating"]
            movie_ratings_list.append(movies[movie]["rating"])
        avg_rating = running_total / len(movies)

        median_rating = None
        sorted_list = sorted(movies.items(), key=lambda x: x[1]['rating'])
        median_index = len(sorted_list) // 2
        if len(sorted_list) % 2 == 0:
            median_rating = float(
                math.ceil((sorted_list[median_index][1]['rating'] + sorted_list[median_index + 1][1]['rating']) / 2))
        else:
            median_rating = sorted_list[median_index][1]['rating']

        best_movie = sorted_list[-1]
        worst_movie = sorted_list[0]

        print(f"Average rating: {avg_rating}")
        print(f"Median rating: {median_rating}")
        print(f"Best movie: {best_movie[1]['title']}, rating: {best_movie[1]['rating']}, year: {best_movie[1]['year']}")
        print(
            f"Worst movie: {worst_movie[1]['title']}, rating: {worst_movie[1]['rating']}, year: {worst_movie[1]['year']}")

    def _command_random_movie(self):
        movies = self._storage.list_movies()
        movies_list = list(movies.items())
        random_movie = random.choice(movies_list)
        print(f"Your movie for tonight: {random_movie[0]}, it's rated {random_movie[1]['rating']}")

    def _command_search_movie(self):
        movies = self._storage.list_movies()
        search_query = input(Fore.YELLOW + "Enter part of movie name: ")
        store_query = search_query
        search_query = search_query.lower()
        print(Fore.WHITE)
        counter = 0
        for movie in movies:
            movie_name = movie.lower()
            if movie_name.find(search_query) != -1:
                print(f"{movie}, {movies[movie]}")
                counter += 1
        if counter == 0:
            print(f"The movie {store_query} does not exist. Did you mean: ")
            similar_results = process.extract(search_query, list(movies.keys()))
            for el in similar_results:
                print(el[0])

    def _sort_key(self, el):
        return el[1]['rating']

    def _command_sorted_movies(self):
        movies = self._storage.list_movies()
        movies_list = list(movies.items())
        movies_list.sort(key=self._sort_key, reverse=True)
        for movie_item in movies_list:
            print(f"{movie_item[0]}, {movie_item[1]}")

    def _read_html(self, file_path):
        """ Read a html file """
        with open(file_path, "r") as handle:
            return handle.read()

    def _write_html(self, html, data):
        """ Write the newly constructed html string to a file """
        result = html.replace('__TEMPLATE_MOVIE_GRID__', data);
        result = result.replace('__TEMPLATE_TITLE__', "My Movie App")
        with open('_static/index_template.html', "w") as file:
            file.write(result);

    def _serialize_movie(self, movie_info):
        """ Serialize a single movie's info """
        output = '<li>'
        output += '<div class="movie">'
        if 'poster_img_url' in movie_info:
            output += f"<img class='movie-poster' src={movie_info['poster_img_url']} /><br/>\n"
        if 'title' in movie_info:
            output += f"<div class='movie-title'>{movie_info['title']}</div><br/>\n"
        if 'year' in movie_info:
            output += f"<div class='movie-year'>{movie_info['year']}</div><br/>\n"
        output += "</div>"
        output += '</li>'
        return output

    def _get_data(self, data):
        """ Serialize all animal data """
        output = ''
        if type(data) == str:
            return data

        for movie_info in data:
            output += self._serialize_movie(data[movie_info])
        return output

    def _generated_website(self):
        html = self._read_html("_static/index_template.html")
        movies = self._storage.list_movies()
        html_data = self._get_data(movies)
        self._write_html(html, html_data)
        print("Website was generated successfully.")

    def run(self):

        while True:
            print(Fore.GREEN)
            print("Menu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Generate website")
            print("\n")

            print(Fore.WHITE)

            user_input = input(Fore.YELLOW + "Enter choice (0-9): ")
            print(Fore.WHITE)

            if user_input == "0":
                exit("Bye!")
            elif user_input == "1":
                self._command_list_movies()
            elif user_input == "2":
                title = input("Enter movie title: ")
                self._storage.add_movie(title)
            elif user_input == "3":
                title = input("Enter movie title: ")
                self._storage.delete_movie(title)
            elif user_input == "4":
                title = input("Enter movie title: ")
                rating = float(input("Enter new movie rating: "))
                self._storage.update_movie(title, rating)
            elif user_input == "5":
                self._command_movie_stats()
            elif user_input == "6":
                self._command_random_movie()
            elif user_input == "7":
                self._command_search_movie()
            elif user_input == "8":
                self._command_sorted_movies()
            elif user_input == "9":
                self._generated_website()

            print()
            check_key_pressed = input("Press enter to continue")

