
"""
Configuration settings for FIFA21 ETL pipeline
"""
import os 
from pathlib import Path

#Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

#Define log directory
LOG_DIR= PROJECT_ROOT/ 'logs'

#Create directory
LOG_DIR.mkdir(exist_ok= True)



#=======EXTRACT SETTINGS=====
#File paths and directories

DATA_DIR = "data"
RAW_SUBDIR = "raw"
RAW_FILENAME = "fifa21 raw data v2.csv"
    
CSV_LOW_MEMORY = False 

#======TRANSFORM SETTINGS=========


#Column names(Source Data)

COL_WEIGHT = 'Weight'
COL_HEIGHT = 'Height'
COL_WAGE   = 'Wage'
COL_VALUE  = 'Value'
COL_HITS   = 'Hits'
COL_RELEASE_COLUMN = 'Release Clause'

#Column names(Transformed)

COL_WEIGHT_KG = 'Weight(KG)'
COL_HEIGHT_CM = 'Height(cm)'
COL_WAGES_K = "Wages(€K)"

#Columns to Drop

COLUMNS_TO_DROP = ['W/F', 'SM', 'IR','Contract']

#Other parameters
DROP_AXIS = 1

#=====LOAD SETTING====

#Output directories
PROCESSED_SUBDIR = 'processed'

#Output filenames
DEFAULT_OUTPUT_FILENAME = 'fifa_cleaned'
SUMMARY_FILENAME = 'data_summary.txt'

#File formats
DEFAULT_OUTPUT_FORMATS= ['csv', 'excel', 'json','parquet']


#File Encoding
FILE_ENCODING = 'utf-8'

#Pandas parameter
SAVE_INDEX = False #For csv,excel & parquet
EXCEL_ENGINE = 'openpyxl'
PARQUET_ENGINE = 'pyarrow'
JSON_ORIENT = 'records'
JSON_INDENT = 2

#Summary report settings
SUMMARY_SEPARATOR = "=" * 60
SUMMARY_SUBSEPARATOR = "-" * 60

#File size calculation
MB_CONVERSION = 1024 * 1024 

#=====Logging settings======
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_DIR = 'logs'
LOG_FILENAME_PREFIX = 'pipeline'

