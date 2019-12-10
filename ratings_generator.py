import csv
import random

NUMBER_OF_BOOKS = 30

with open('./dataset/ratings.csv', 'w') as my_csv_file:

    csv_writer = csv.writer(my_csv_file)
    rows = []
    for user_ID in range(30):
        for _ in range(10): 
            book_ID = str(random.randint(0, 30))
            book_rating = str(random.randint(0, 5))
            data_entry = [str(user_ID), book_ID, book_rating]  
            csv_writer.writerow(data_entry)