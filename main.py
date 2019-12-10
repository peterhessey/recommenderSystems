from csvScripts import csvUpdater
import pandas as pd
import numpy as np 

BOOKS = 'books.csv'
RATINGS = 'ratings.csv'
USERS = 'user_profiles.csv'

def setUpMatrix():
	books_file = csvUpdater(BOOKS)
	ratings_file = csvUpdater(RATINGS)
	users_file = csvUpdater(USERS)

	books_data = books_file.getData()
	books_df = pd.DataFrame(books_data, columns = ['book_ID', 'book_title', 'genres'])
	
	ratings_data = ratings_file.getData()
	ratings_df = pd.DataFrame(ratings_data, columns = ['user_ID', 'book_ID', 'rating'])

	ratings = ratings_df.pivot(index = 'user_ID', columns='book_ID', values='rating').fillna(0)
	
	ratings_matrix = ratings.as_matrix()
	ratings_mean = np.mean(R, axis = 1)
	ratings_demeaned = ratings_matrix - ratings_mean.reshape(-1,1)
if __name__ == '__main__':
	setUpMatrix()