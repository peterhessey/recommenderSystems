import csv
import random
import string

NUMBER_OF_BOOKS = 30

with open('./dataset/user_profiles.csv', 'w') as my_csv_file:

    csv_writer = csv.writer(my_csv_file)
    csv_writer.writerow(['user_ID', 'username', 'password'])
    valid_chars = string.ascii_lowercase
    for user_ID in range(30):
        username = ''.join(random.choice(valid_chars) for _ in range(6))
        password = 'password'
        data_entry = [str(user_ID), username, password] 
        csv_writer.writerow(data_entry)