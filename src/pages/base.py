import requests
import pandas as pd

class Base:
    """
    Class handles all connection to the CSV and returns a DataFrame from it's initialization.
    """
    def __init__(self):
        self.df = pd.read_csv('/Users/investmentguy/Tableau_Bonfire_124/bonfire_124_streamlit_app/bonfire_124_streamlit_app/src/data/student_info.csv')
        self.get_data()
    
    
if __name__ == "__main__":
    c = Base()