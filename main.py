"""FIFA 21 Data Pipeline- Main Orchestrator

This script runs the complete ETL (Extract, Transform, Load) pipeline:
1.Extract: Load raw data from CSV
2.Transform: Clean and process the data
3.Load: Save clean data in multiple formats

"""

import os
import sys
import logging  
from datetime import datetime 

# Add project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir  # main.py is at project root (simple_project1/)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import utilities
from eti_pipeline.src.utilis.path_utilis import PROJECT_ROOT
from eti_pipeline.src.utilis.logger_utilis import setup_logging

#Import modules
from config.config import (
    DATA_DIR,
    RAW_SUBDIR,
    RAW_FILENAME,
    LOG_DIR,
    LOG_FILENAME_PREFIX,
    LOG_FORMAT,
    LOG_LEVEL,
    MB_CONVERSION,
    SUMMARY_SEPARATOR,
    SUMMARY_SUBSEPARATOR,
    DEFAULT_OUTPUT_FILENAME,
    DEFAULT_OUTPUT_FORMATS,
    LOG_FILENAME_PREFIX   
)

from eti_pipeline.src.extract.extract import load_raw_data
from eti_pipeline.src.transform.transform import transform_fifa_data
from eti_pipeline.src.load.save_data import save_cleaned_data, save_summary_statistics 


#logging configurations

# Setup logging with file handler
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f'{LOG_DIR}/{LOG_FILENAME_PREFIX}_{timestamp}.log'

# Setup logger (will configure with both file and console output)
import logging
logger = setup_logging(__name__)

# Add file handler to the existing logger
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


def run_pipeline():
    """
    RUN the complete Fifa data pipeline with comprehensive eerror handling
    """

    print('=' * 60)
    print(" FIFA 21 Data Pipeline")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        #====================================================================
        #   STEP 1: EXTRACT - Load Raw Data
        #====================================================================
        
        print("\n STEP 1: EXTRACT")
        print("=" * 60)
        
        try:
            raw_data = load_raw_data()

        except FileNotFoundError as e:
            print("\n" + "=" * 60)
            print("❌ PIPELINE FAILED - INPUT FILE NOT FOUND")
            print("=" * 60)
            logging.critical(str(e))
            print("\n💡 Solution: Ensure CSV file exists in data/raw/ folder")
            return None

        except pd.errors.EmptyDataError as e:
            print("\n" + "=" * 60)
            print("❌ PIPELINE FAILED - INPUT FILE IS EMPTY")
            print("=" * 60)
            logging.critical(str(e))
            return None
            
        except pd.errors.ParserError as e:
            print("\n" + "=" * 60)
            print("❌ PIPELINE FAILED - CSV FILE IS CORRUPTED")
            print("=" * 60)
            logging.critical(str(e))
            print("\n💡 Solution: Check that file is a valid CSV")
            return None

        #====================================================================
        #   STEP 2: TRANSFORM - Clean the Data
        #====================================================================


        print("\n STEP 2: TRANSFORM")
        print("=" * 60)
        
        try:
            cleaned_data = transform_fifa_data(raw_data)
            print(f"✅ Transform complete!")
            print(f" 📊 Cleaned data: {cleaned_data.shape[0]:,} rows × {cleaned_data.shape[1]} columns")
            
        except KeyError as e:
            print("\n" + "=" * 60)
            print("❌ PIPELINE FAILED - MISSING REQUIRED COLUMN")
            print("=" * 60)
            logging.critical(f"Missing column in CSV: {e}")
            print(f"\n💡 Required column not found: {e}")
            print("   Check that CSV has all expected columns")
            return None

        #===================================================================
        #  STEP 3: LOAD - Save cleaned data
        #===================================================================


        print("\n STEP 3: LOAD")
        print("=" * 60)
        
        try:
            saved_files = save_cleaned_data(cleaned_data, base_filename='fifa21_cleaned')
            print(f"✅ Load Complete!")
            
        except PermissionError as e:
            print("\n" + "=" * 60)
            print("❌ PIPELINE FAILED - CANNOT WRITE OUTPUT FILES")
            print("=" * 60)
            logging.critical(f"Permission denied: {e}")
            print("\n💡 Solution: Check that data/processed/ folder is writable")
            return None

        # Save in multiple formats

        saved_files =save_cleaned_data(cleaned_data, base_filename = DEFAULT_OUTPUT_FILENAME, formats = DEFAULT_OUTPUT_FORMATS)

        #Save summary statistics

        logging.info(f" Load Complete!")

        #==================================================================
        # PIPELINE SUMMARY
        #==================================================================
        print("\n" + "-" * 60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)

        print("\n📊 Summary:")
        print(f"  • Input rows: {raw_data.shape[0]:,}")
        print(f"  • Output rows: {cleaned_data.shape[0]:,}")
        print(f"  • Columns removed: {raw_data.shape[1] - cleaned_data.shape[1]}")
        print(f"  • Files created: {len(saved_files)}")

        print("\n📁 Output Files:")
        for fmt, path in saved_files.items():
            file_size = os.path.getsize(path) / (1024*1024)
            print(f"  • {fmt.upper()}: {file_size:.2f} MB")

        print("\n" + "-" * 60)
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        return cleaned_data
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("⚠️  PIPELINE INTERRUPTED BY USER")
        print("=" * 60)
        logging.warning("Pipeline interrupted by user (Ctrl+C)")
        return None
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ PIPELINE FAILED - UNEXPECTED ERROR")
        print("=" * 60)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        logging.critical(f"Unexpected error: {str(e)}", exc_info=True)
        print("\n💡 Please check the log file for details")
        raise  # Re-raise for debugging

#Run the pipeline when the script is executed

if __name__ == "__main__":
    run_pipeline()

    
