# HOW TO RUN

1. Ensure you have python 3.x and pip installed on your machine
2. Navigate to the directory in which the 'requirements.txt' file is stored
3. Run the command 'pip install -r requirements.txt' to install all libraries necessary to run the program
4. Run the command 'python main.py'
5. The system is now live, you will be able to access it from the url 'localhost:5000/'
6. The demo login is the username 'test' and password 'password'


# System Features

- My system uses CSV files to store the dataset
- The dataset was built by me with reference to GoodReads.com. It contains:
    - 30 books in book.csv 
    - 300 (randomly generated) ratings in ratings.csv, 10 per user.
    - 30 users in user_profiles.csv

- User profiling is simply done through a user_ID, username and password. 
    - You can access any login by opening ratings.csv and using the login provided
    - A cookie with key value 'WebTechCookie' stores the current users' user_ID

- The recommendation algorithm uses pandas and numpy to produce unique book
  recommendations for each user. When the user logs in, the algorithm is run and
  the most suitable books are selected. The algorithm uses the users ratings 
  combined with the ratings of all other users to calculate which books the user
  is most likely to want to read.

- The interface is a simply static website with dynamic update capability. From
  the home page a user can:
    - View all the books they've already rated
    - See the books recommended for them to read
    - Create new ratings for any book or update ratings for already rated books

- The user can also register a new account from the login page if desired, 
  however it comes without any previous ratings so new ratings will have to be
  made for the recommendation algorithm to work.