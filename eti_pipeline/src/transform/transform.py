import sys
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import logging
from datetime import datetime 

#Add project root to path
# 1. Path setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
     sys.path.insert(0, project_root)


# 2. Import utilities
from eti_pipeline.src.utilis.path_utilis import PROJECT_ROOT
from eti_pipeline.src.utilis.logger_utilis import setup_logging
from eti_pipeline.src.utilis.file_utilis import load_csv_safe

try:
     from .string_converter_wages import convert_wages_thousands
     from .string_converter_clause import convert_clause_thousands 
     from .string_converter_hits import convert_hits_column
     from .string_converter_height import convert_height_column 
     from .string_converter_weight import convert_weight_column
     from .string_converter_value import convert_value_column 
except:
     from string_converter_wages import convert_wages_thousands
     from string_converter_clause import convert_clause_thousands
     from string_converter_hits import convert_hits_column
     from string_converter_height import convert_height_column 
     from string_converter_weight import convert_weight_column
     from string_converter_value import convert_value_column  


from config.config import(
     #File Paths
     DATA_DIR,
     RAW_FILENAME,
     RAW_SUBDIR,

     #Pandas paremeter
     CSV_LOW_MEMORY,

     #Original columns
     COL_HEIGHT,
     COL_HITS,
     COL_RELEASE_COLUMN,
     COL_VALUE,
     COL_WAGE,
     COL_WEIGHT,
     
     #New columns(transformed)
     COL_WAGES_K,
     COL_HEIGHT_CM,
     COL_WEIGHT_KG,
     
     #Drop columns
     COLUMNS_TO_DROP,

     #Other Parameter
     DROP_AXIS,
     SUMMARY_SEPARATOR,

     #log settings
     LOG_FORMAT,
     LOG_LEVEL
     
)

# 4. Setup logger
logger = setup_logging(__name__)

def transform_weight_column(df):
     """Renaming the weight column to weight(kg)"""
     df=df.copy()
     df.rename(columns={COL_WEIGHT:COL_WEIGHT_KG}, inplace=True)

     df[COL_WEIGHT_KG]=df[COL_WEIGHT_KG].apply(convert_weight_column)
     return df
   
#Rename the existing height column and converting string to interger
def transform_height_column(df):
        
     """"Renaming the height column to height(cm)"""
     df = df.copy()
     df.rename(columns={COL_HEIGHT: COL_HEIGHT_CM}, inplace=True)

     #Removing the "cm" from the string rows
     df[COL_HEIGHT_CM]=df[COL_HEIGHT_CM].apply(convert_height_column)
     return df

#Rename the value column and convert the existing rows into integers

def transform_value_column(df):
        
     """converts string values to integers"""
     df= df.copy()
     df[COL_VALUE]=df[COL_VALUE].apply(convert_value_column)
     return df 

def transform_wage_column(df):
        
        
        """Converts wage to standardized thousands(K)"""
        df = df.copy()

        #Rename the column
        
        df.rename(columns={COL_WAGE:COL_WAGES_K},inplace=True)
        
        df[COL_WAGES_K]= df[COL_WAGES_K].apply(convert_wages_thousands)
        return df

def transform_release_column(df):
     """Convert Release clause column to standardize column"""
     df = df.copy()

     df[COL_RELEASE_COLUMN]=df[COL_RELEASE_COLUMN].apply(convert_clause_thousands)
     return df 

def transform_hits_column(df):
     """Convert Hits column to standardized format"""
     ## Convert all values to strings (NaN becomes 'nan' string, but pd.isna() still catches it)

     df = df.copy()
     df[COL_HITS]=df[COL_HITS].astype(str)
     df[COL_HITS]=df[COL_HITS].apply(convert_hits_column)
     return df 

def delete_four_column(df):
     """Converts the name column into a standardize format"""

     df = df.copy()
     df=df.drop(COLUMNS_TO_DROP, axis= DROP_AXIS)
     return df     

def transform_fifa_data(raw_data):
     """Master function that applies all the transformation in sequence
     
     Args:
          raw_data(pd.Dataframe): Raw Fifa Dataset
          
     Returns:
          pd.Dataframe: Fully transformed dataset
          
    """
     
     logging.info("Starting transformation pipeline----")

     # Step 1: Cleaning column names

     logging.info('\n - Cleaning column names---')
     df = raw_data.copy()

     # Step 2: Transforming value columns
     df = transform_value_column(df)

     # Step 3: Transform weight column

     df = transform_weight_column(df)

     # Step 4: Transform wage column

     df = transform_wage_column(df)

     # Step 5: Transform height column

     df = transform_height_column(df) 

     # Step 6: Transform hits column

     df = transform_hits_column(df)

     # Step 7: transform release column

     df = transform_release_column(df)

     # Step 8: Deleted four columns

     df= delete_four_column(df)

     logging.info('====Transformation Complete!====')
     return df 

if __name__ == "__main__":

     #Configure logging for standalone testing
     logging.basicConfig(
          level=LOG_LEVEL,
          format=LOG_FORMAT,
          handlers=[
               logging.StreamHandler()
          ]
     )

     #Test transformation differently
     import os

     logging.info("Test transformation module")
     logging.info( SUMMARY_SEPARATOR)

     #Load sample data
     script_dir = os.path.dirname(os.path.abspath(__file__))
     project_root = os.path.join(script_dir, '..', '..','..')
     file_location = os.path.join(project_root, DATA_DIR, RAW_SUBDIR, RAW_FILENAME)

     # Debug output
     logging.info(f"\nScript dir:{script_dir}")
     logging.info(f"Project root:{os.path.abspath(project_root)}")
     logging.info(f"File location:{os.path.abspath(file_location)}")
     logging.info(f"File exists?{os.path.exists(file_location)}\n")

     raw_data = pd.read_csv(file_location, low_memory=CSV_LOW_MEMORY)

     logging.info(f"Input shape:{raw_data.shape}")

     #Run transformations
     cleaned_data=transform_fifa_data(raw_data)

     logging.info(f"\nOutput shape:{cleaned_data.shape}")
     logging.info(f"\nTransformed columns: {list(cleaned_data.columns[:10])}")
     logging.info(f"\nSample of  transformed data:")
     logging.info(cleaned_data.head(3))

     #Show some statistics

     #print(f"\nData quality check:")
     #print(f"Missing values:{cleaned_data.isnull().sum()}")
     #print(f"Duplicate rows: {cleaned_data.duplicated().sum()}")








    
    

    





