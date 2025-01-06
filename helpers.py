"""
Helper functions required for the main scripts.

Author:
    Cameron Trotter (cater@bas.ac.uk)

Date:
    6/01/2025
"""
import pandas as pd

def read_csv_to_df(path):
    """
    Read a CSV file into a pandas dataframe.
    
    Args:
        path (str): The path to the CSV file.
        
    Returns:
        df (pandas.core.frame.DataFrame): A pandas dataframe containing the data from the CSV file.
    """
    df = pd.read_csv(path)
    return df