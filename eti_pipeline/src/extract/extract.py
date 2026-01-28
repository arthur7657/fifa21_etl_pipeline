import sys
import os
import pandas as pd
import logging

#Setup path first

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..')))
from datetime import datetime
from eti_pipeline.src.utilis.path_utilis import PROJECT_ROOT
from eti_pipeline.src.utilis.logger_utilis import setup_logging 
from eti_pipeline.src.utilis.file_utilis import load_csv_safe



from config.config import(
    DATA_DIR,
    RAW_FILENAME,
    RAW_SUBDIR,
    CSV_LOW_MEMORY,
    LOG_FORMAT,
    LOG_LEVEL
)

# Setup logger
logger = setup_logging(__file__)

def load_raw_data(file_path=None):

    """Load raw fifa21 data from csv file
       Raises:
        FileNotFoundError: If CSV file doesn't exist
        pd.errors.EmptyDataError: If CSV is empty
        pd.errors.ParserError: If CSV is corrupted
    
    """
    if file_path is None:
        #Get to the script's directory and go to the project path
        script_dir = os.path.dirname(os.path.abspath(__file__))

        #Go up: Extract- src-eti_pipeline-simple_project1
        project_root = os.path.join(script_dir,'..','..','..')
        file_path = os.path.join(project_root, DATA_DIR,RAW_SUBDIR,RAW_FILENAME)

    logging.info(f"\n🔄 Extract: Loading data from: {os.path.basename(file_path)}")
    logging.info(f" 📂 Location: {file_path}")

    # load_csv_safe now raises exceptions instead of returning None
    df = load_csv_safe(file_path, low_memory=CSV_LOW_MEMORY)
    
    logging.info(f"✅ Extraction complete!")
    return df
    
# Test code
if __name__ == "__main__":
    #logging configuration

    logging.basicConfig(
    level =LOG_LEVEL,
    format = LOG_FORMAT,
    handlers = [
        logging.StreamHandler()
    ]
     )
    logging.info("Testing Extract Module")
    logging.info("=" * 50)

    data = load_raw_data()

    if data is not None:
        logging.info(f"\nFirst 5 rows:")
        logging.info(data.head(5))

    else:
        logging.info("Failed to load")

