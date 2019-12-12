import os, sys, csv

class csvUpdater():

    def __init__(self, csv_filename):
        """Constructor function for csvUpdater() class.
        
        Arguments:
            csv_filename {str} -- Filename of the csv file to be manipulated
            by the updater object.
        """
        self.csv_file = './dataset/' + csv_filename


    def getData(self):
        """Gets and returns the data in the CSV file
        
        Returns:
            [[int/str]] -- The csv data
        """
        with open(self.csv_file, 'r') as csv_to_return:
            csv_reader = csv.reader(csv_to_return)
            data = []
            for row in csv_reader:
                if row != [] and csv_reader.line_num != 1:
                    new_row = []
                    for item in row:
                        
                        try:
                            new_row.append(int(item))
                        except:
                            new_row.append(item)

                    data.append(new_row)
                        
            return data


    def delete(self, primary_key, secondary_key=-1):
        """Delete a row from the CSV file
        
        Arguments:
            primary_key {int} -- Primary key of the row
        
        Keyword Arguments:
            secondary_key {int} -- Secondary key if the csv files uses 
            composite keys. (default: {-1})
        """
        use_2_keys = False if secondary_key == -1 else True

        with open(self.csv_file, 'r') as csv_to_read:
            with open('./dataset/copy.csv', 'w') as csv_to_write:
                reader = csv.reader(csv_to_read)
                writer = csv.writer(csv_to_write)

                for row in reader:
                    if row != []:
                        if not use_2_keys:
                            if row[0] != primary_key:
                                writer.writerow(row)
                        else:
                            if row[0] != primary_key or row[1] != secondary_key:
                                writer.writerow(row)

        os.remove(self.csv_file)
        os.rename('./dataset/copy.csv', self.csv_file)


    def update(self, primary_key, column_num, new_val, secondary_key=-1):
        """Updates a row in the CSV file.
        
        Arguments:
            primary_key {int} -- Primary key of the row
            column_num {int} -- Column to be updated
            new_val {int} -- The value to be put in the row
        
        Keyword Arguments:
            secondary_key {int} -- Secondary key in case the CSV file uses 
            composite keys. (default: {-1})
        
        Returns:
            bool -- True if succeeded, false otherwise
        """
        use_2_keys = False if secondary_key == -1 else True
        updated = False

        with open(self.csv_file, 'r') as csv_to_read:
            with open('./dataset/copy.csv', 'w') as csv_to_write:
                reader = csv.reader(csv_to_read)
                writer = csv.writer(csv_to_write)

                for row in reader:
                    if row != []:
                        if not use_2_keys:
                            if row[0] != str(primary_key):
                                writer.writerow(row)
                            else:
                                row = self.getNewRow(row, column_num, new_val)
                                writer.writerow(row)
                                updated = True
                        else:
                            if row[0] != primary_key or row[1] != secondary_key:
                                writer.writerow(row)
                            else:
                                row = self.getNewRow(row, column_num, new_val)
                                writer.writerow(row)
                                updated = True
        if not updated:
            return False
        else:
                
            os.remove(self.csv_file)
            os.rename('./dataset/copy.csv', self.csv_file)
            return True


    def newRow(self, new_row):
        """Writes a new row into the CSV file
        
        Arguments:
            new_row {[int/str]} -- The new row to write
        """
        valid_row = True
        with open(self.csv_file, 'r') as csv_to_update:
            csv_reader = csv.reader(csv_to_update)

            for row in csv_reader:
                if row != []:
                    if len(row) != len(new_row):
                        print('Invalid input, incorrect number of values.')
                        valid_row = False
                        break

        if valid_row:
            with open(self.csv_file, 'a') as csv_to_append:
                csv_writer = csv.writer(csv_to_append)
                try:
                    csv_writer.writerow(new_row)
                except:
                    print('Row not writeable.')


    def validateLogin(self, username, password):
        """Given a username and password, checks if it is a registered account
        and that the password is correct.
        
        Arguments:
            username {str} -- The username
            password {str} -- The password
        
        Returns:
            bool, int -- True if the user logs in, as well as the ID of the 
            logged in user (used for cookies)
        """
        with open(self.csv_file, 'r') as user_logins_file:
            csv_reader = csv.reader(user_logins_file)
            for row in csv_reader:
                if row != []:
                    if row[1] == username and row[2] == password:
                        return True, row[0]

        
        return False, -1


    def getNewRow(self, row, column_num, new_val):
        """Creates a new row to write into the CSV file
        
        Arguments:
            row {[int]} -- The old row
            column_num {int} -- The column to rewrite
            new_val {int} -- The value to write into the row
        
        Returns:
            [int] -- The newly created row
        """
        new_row = []
        for i in range(len(row)):
            if i != column_num:
                new_row.append(row[i])
            else:
                new_row.append(str(new_val))
        
        return new_row