##############################################################################
'''

Web Techonlogies Coursework - Recommender Systems

Completed as part of MEng in Computer Science at Durham University

Recommender systems code largely based on tutorial that can be found at:
https://beckernick.github.io/matrix-factorization-recommender/

'''
##############################################################################
from csvScripts import csvUpdater
from scipy.sparse.linalg import svds
from flask import Flask, redirect, url_for, request, render_template, make_response
import pandas as pd
import numpy as np 

# set up Flask app
app = Flask(__name__)

# dataset and user profile files
BOOKS = 'books.csv'
RATINGS = 'ratings.csv'
USERS = 'user_profiles.csv'


def setUpMatrix():
	"""Initialise the dataframes for the recommender algorithm. Reads in data
	from the CSV files, converts the data into Pandas dataframes. Then 
	performs matrix manipulation in order to provide a suitable data format for
	the recommender algorithm. 

	Finally uses matrix singularisation to get predicted ratings for each user
	and book.
	
	Returns:
		DataFrame, DataFrame, DataFrame -- Books, ratings and predicited 
		ratings dataframes.
	"""
	books_file = csvUpdater(BOOKS)
	ratings_file = csvUpdater(RATINGS)
	users_file = csvUpdater(USERS)

	books_data = books_file.getData()
	books_df = pd.DataFrame(books_data, columns = ['book_ID', 'book_title', 'genres'])
	
	ratings_data = ratings_file.getData()
	ratings_df = pd.DataFrame(ratings_data, columns = ['user_ID', 'book_ID', 'book_rating'], dtype = int)
	ratings = ratings_df.pivot(index = 'user_ID', columns='book_ID', values='book_rating')

	ratings_mean = np.array(ratings.mean(axis=1))
	ratings_demeaned = ratings.sub(ratings.mean(axis=1), axis=0)
	ratings_demeaned = ratings_demeaned.fillna(0).values

	U, sigma, Vt = svds(ratings_demeaned, k = 25)
	sigma = np.diag(sigma)

	all_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + ratings_mean.reshape(-1, 1)
	predictions_df = pd.DataFrame(all_predicted_ratings, columns = ratings.columns)

	return books_df, ratings_df, predictions_df


def getRecommendedBooks(user_ID, books_df, ratings_df, predictions_df, num_of_recs=3):
	"""Uses the dataframes to format and return a set of recommended books for 
	the user based on what they've rated previously.
	
	Arguments:
		user_ID {int} -- The ID value of the user
		books_df {DataFrame} -- DataFrame storing book data
		ratings_df {DataFrame} -- DataFrame storing book ratings data
		predictions_df {DataFrame} -- DataFrame storing predicted ratings for
		each user and book.
	
	Keyword Arguments:
		num_of_recs {int} -- Number of books to recommend (default: {3})
	
	Returns:
		DataFrame -- DataFrame of recommended books and their associated data
	"""
	# get user predictions and sort them
	user_predictions = predictions_df.iloc[user_ID].sort_values(ascending=False)

	# merge user and book data
	
	user_ratings = ratings_df[ratings_df.user_ID == user_ID]

	user_book_data_merged = (user_ratings.merge(books_df, how='left', left_on='book_ID', right_on='book_ID',).
								sort_values(['book_rating'], ascending=False)
							)

	# create recommended books dataframe
	recommended_books = (books_df[~books_df['book_ID'].isin(user_book_data_merged['book_ID'])].
			merge(pd.DataFrame(user_predictions).reset_index(), how = 'left',
				left_on = 'book_ID',
				right_on = 'book_ID').
			rename(columns = {user_ID: 'Predictions'}).
			sort_values('Predictions', ascending = False).
						iloc[:num_of_recs, :-1]
						)

	return recommended_books


@app.route('/')
def index():
	if request.cookies.get('WebTechCookie') == None:
		return redirect(url_for('loadLoginPage', invalid_login=0))
	else:
		return redirect(url_for('loadHomePage'))


@app.route('/login/<invalid_login>')
def loadLoginPage(invalid_login):
	print('loading login page')
	return render_template('login.html', invalid=int(invalid_login))


@app.route('/attemptLogin', methods=['POST'])
def login():
	user = request.form['username']
	password = request.form['password']

	loginChecker = csvUpdater(USERS)

	valid_login, user_ID = loginChecker.validateLogin(user, password)

	if valid_login:
		resp = redirect(url_for('loadHomePage'))
		resp.set_cookie('WebTechCookie', user_ID)
	else:
		resp = redirect(url_for('loadLoginPage', invalid_login=1))
		resp.set_cookie('WebTechCookie', '', expires=0)

	return resp


@app.route('/home/')
def loadHomePage():
	user_ID = int(request.cookies.get('WebTechCookie'))
	if user_ID != None:
		# getting username from csv files
		csv_data_getter = csvUpdater(USERS)
		username = csv_data_getter.getData()[0][1]
		# data to send to the html form
		data = {'username':username}

		books_df, ratings_df, predictions_df = setUpMatrix()  
		
		# the books to recommend 
		recommendations = getRecommendedBooks(user_ID, books_df, ratings_df, predictions_df)
		# all the ratings of the logged in user
		user_ratings = ratings_df[ratings_df.user_ID == user_ID]
		# all the books that have been rated by the logged in user
		user_book_data_merged = (user_ratings.merge(books_df, how='left', left_on='book_ID', right_on='book_ID',).
									sort_values(['book_rating'], ascending=False)
								)

		# books already rated
		user_books = []
		for i in range(len(user_book_data_merged)):
			df_row = user_book_data_merged.iloc[i]
			user_book = [df_row['book_title'], df_row['book_rating']]
			user_books.append(user_book)


		# books to recommend
		book_recs = []
		for i in range(len(recommendations)):
			df_row = recommendations.iloc[i]
			recommendation = df_row['book_title']
			book_recs.append(recommendation)

		
		all_books = books_df.values
		data['all_books'] = all_books	
		data['user_books'] = user_books
		data['recs'] = book_recs

		return render_template('index.html', data=data)
	else:
		return 'Please login to access this page'


@app.route('/rate', methods=['POST'])
def newRating():
	book_ID = request.form['book_title']
	rating = int(request.form['rating'])
	user_ID = request.cookies.get('WebTechCookie')

	if rating >= 0 and rating <= 5:
		rating_updater = csvUpdater(RATINGS)
		if not rating_updater.update(book_ID, 1, rating):
			new_row = [user_ID, book_ID, rating]
			rating_updater.newRow(new_row)

		return redirect(url_for('loadHomePage'))




@app.route('/logout')
def logout():
		
	resp = redirect(url_for('loadLoginPage', invalid_login=0))
	resp.set_cookie('WebTechCookie', '', expires=0)

	return resp


if __name__ == '__main__':
	app.debug = True
	app.run()
