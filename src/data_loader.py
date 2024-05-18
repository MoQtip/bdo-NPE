import pandas as pd
import config

class ExcelDataLoader:
    """
    A class for loading node data from an Excel file specified in the application's configuration.
    
    Attributes:
        file_path (str): The path to the Excel file containing node data.
    """
    
    def __init__(self, file_path):
        """
        Initializes the ExcelDataLoader with the path to the Excel file.
        
        Parameters:
            file_path (str): The path to the Excel file to load.
        """
        self.file_path = file_path

    def load_excel_data(self):
        """
        Loads the node data from the Excel file specified at initialization.
        
        Returns:
            DataFrame: A Pandas DataFrame containing the loaded node data. The structure of the DataFrame
            will align with the structure of the Excel file, where each row represents a node and columns
            represent node attributes such as Node ID, Name, Type, etc.
        """
        return pd.read_excel(self.file_path, sheet_name=config.SHEET_NAME_ALL)
