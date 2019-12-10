from dataset_update import csvUpdater

if __name__ == '__main__':
	book_updater = csvUpdater('ratings.csv')
	book_updater.delete('29', '24')