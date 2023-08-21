import pandas as pd
from dotenv import load_dotenv
import pymongo
import os

class ToMongo():
    """
    Defined method of this class are:
    create_df: Takes in two file paths and cleans the data. Converts both into DataFrames and then inner joins
                the data to get the students from both classes only.
    upload_students: Uploads the DataFrame to the Mongo Database.
    Wrangle: cleans the data, allowing for better readibility. Returns as a pandas DataFrame when complete.
    """

    def __init__(self, user=os.getenv('USERNAME'), password=os.getenv('PASSWORD')):
        # Load the .env variables
        load_dotenv()
        self.user = user
        self.password = password
        self.mongo_url = os.getenv('MONGO_URL')
        # Connecting to PyMongo
        self.client = pymongo.MongoClient(self.mongo_url)
        # Creating a database
        self.db = self.client.db
        # Creating a collection
        self.cards = self.db.cards
        # Set dataframe index to the id column
        # self.df.set_index('id', inplace=True)
    
    def create_df(self, filepath1, filepath2):
        self.df = self.wrangle(filepath1)
        self.df2 = self.wrangle(filepath2)
        column_list = ["school","sex","age","address","famsize","Pstatus","Medu","Fedu","Mjob","Fjob","reason","nursery","internet"]
        self.df_final.columns = self.df_final.columns.str.replace(' ', '_').str.strip().str.lower()
        self.df_final = self.df.merge(self.df1, on=column_list, how='outer')
        self.df_final[self.df_final['guardian_x'].isna() == True]
        self.df_final[self.df_final['traveltime_x'].isnull() == True]
        self.df_final.dropna(inplace=True)
    
    def upload_students(self):
        """
        Upload all our students to MongoDB, one by one. While also dropping
        the old so the copy doesn't double itself.
        """
        self.cards.drop()
        for i in self.df.index:
            self.cards.insert_one(self.df.loc[i].to_dict())

        return self.df_final

if __name__ == '__main__':
    c = ToMongo()
    print('Connected to the server!')
    c.create_df('/Users/investmentguy/Tableau_Bonfire_124/bonfire_124_streamlit_app/bonfire_124_streamlit_app/student-mat.csv' sep=";",
                '/Users/investmentguy/Tableau_Bonfire_124/bonfire_124_streamlit_app/bonfire_124_streamlit_app/student-por.csv' sep=";")
    print("wrangled the data!")
    c.upload_students()
    print('Uploaded the data!')