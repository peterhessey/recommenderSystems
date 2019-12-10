from csvScripts import csvUpdater
import pandas as pd
import numpy as np 

BOOKS = 'books.csv'
RATINGS = 'ratings.csv'
USERS = 'user_profiles.csv'

if __name__ == '__main__':
	logins = csvUpdater(USERS)
	if logins.validateLogin('test','password'):
		print('Valid login')
	else:
		print('inpe')