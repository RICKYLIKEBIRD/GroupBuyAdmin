class adminUser :

    def __init__(self, db_data_row=None):
        if db_data_row is not None:
            self.user_id = db_data_row[0]
            self.user_name = db_data_row[1]
        else:
            self.user_id = None
            self.user_name = None