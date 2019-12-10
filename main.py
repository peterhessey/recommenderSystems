from csvScripts import csvUpdater

if __name__ == '__main__':
	logins = csvUpdater('user_profiles.csv')
	if logins.validateLogin('test','password'):
		print('Valid login')
	else:
		print('inpe')