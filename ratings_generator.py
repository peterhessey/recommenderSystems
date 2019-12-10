import csv
import random

NUMBER_OF_BOOKS = 30

with open('./dataset/ratings.csv', 'w') as my_csv_file:

    csv_writer = csv.writer(my_csv_file)
    csv_writer.writerow(['user_ID', 'book_ID', 'book_rating'])
    ratings = {}

    for user_ID in range(30):
        ratings_to_make = 10

        while ratings_to_make != 0:
            make_rating = True
            new_book_ID = random.randint(0, 30)

            if user_ID in ratings:
                if new_book_ID in ratings[user_ID]:
                    make_rating = False
            else:
                ratings[user_ID] = []

            if make_rating:
                ratings[user_ID].append(new_book_ID)
                book_rating = random.randint(1, 5)
                row = [str(user_ID), str(new_book_ID), str(book_rating)]
                csv_writer.writerow(row)
                ratings_to_make -= 1