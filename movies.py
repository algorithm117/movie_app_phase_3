# Copy your code from the previous Movies project
from movie_app import MovieApp
from storage_csv import StorageCsv
from storage_json import StorageJson


def main():
    print("\n********** My Movies Database **********\n")
    storage = StorageJson('data.json')
    csv_storage = StorageCsv('data.csv')
    movie_app = MovieApp(csv_storage)
    movie_app.run()


if __name__ == "__main__":
    main()