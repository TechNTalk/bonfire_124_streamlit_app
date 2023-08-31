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
        df1 = self.wrangle(filepath1)
        df2 = self.wrangle(filepath2)
        
        self.df = pd.merge(df1, df2, on=("school","sex",
                                         "age","address",
                                         "family_size","parent_cohab_status",
                                         "mother_education","father_education",
                                         "mother_job","father_job","reason",
                                         "nursery","internet"), how='inner')
        self.df.drop(columns=(self.df.columns[33:50].tolist()),axis= 1, inplace=True)
        grades_column = {
            "first_period_grade_x": "math_first_period_grade", 
            "second_period_grade_x": "math_second_period_grade",
            "final_grade_x": "math_final_grade",
            "first_period_grade_y": "port_first_period_grade",
            "second_period_grade_y": "port_second_period_grade",
            "final_grade_y": "port_final_grade"
                }
        self.df.rename(columns=grades_column, inplace=True)
        self.df.columns = self.df.columns.str.rstrip("_x")
    
    def upload_students(self):
        """
        Upload all our students to MongoDB, one by one. While also dropping
        the old so the copy doesn't double itself.
        """
        self.cards.drop()
        for i in self.df.index:
            self.cards.insert_one(self.df.loc[i].to_dict())
    
    @staticmethod
    def wrangle(filepath):
        df = pd.read_csv(filepath,sep=';')
        df.columns = df.columns.str.lower()

        column_trans = {
            'famsize':'family_size',
            'pstatus':'parent_cohab_status',
            'medu':'mother_education',
            'fedu':'father_education',
            'mjob':'mother_job',
            'fjob':'father_job',
            'traveltime':'travel_time',
            'studytime':'study_time',
            'schoolsup':'school_support',
            'famsup':'family_support',
            'famrel':'family_relationship',
            'freetime':'free_time',
            'goout':'outside_socialness',
            'dalc':'workday_alcohol_drink',
            'walc':'weekend_alcohol_drink',
            'g1':'first_period_grade',
            'g2':'second_period_grade',
            'g3':'final_grade'
            }
        df.rename(columns=column_trans, inplace=True)
        
        df.school = df.school.str.replace('GP', 'Gabriel Pereira').str.replace('MS', 'Mousinho da Silveira')
        df.sex = df.sex.str.replace('F','Female').str.replace('M','Male')
        df.address = df.address.str.replace('U','Urban').str.replace('R','Rural')
        df.family_size = df.family_size.str.replace('LE3', '>or= 3').str.replace('GT3','<3')
        df.parent_cohab_status = df.parent_cohab_status.str.replace('T','Together').str.replace('A','Apart')

        return df

if __name__ == '__main__':
    c = ToMongo()
    print('Connected to the server!')
    c.create_df(r'C:\Users\Owner\Documents\Coding Temple\week_6\day_3\student\student-mat.csv',
                r'C:\Users\Owner\Documents\Coding Temple\week_6\day_3\student\student-por.csv')
    print("wrangled the data!")
    c.upload_students()
    print('Uploaded the data!')