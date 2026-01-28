import pandas as pd
import os
import re 
import sqlite3
from sqlalchemy import create_engine
import sys
import logging
from datetime import datetime

# Add project root to path FIRST
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import utilities
from eti_pipeline.src.utilis.path_utilis import PROJECT_ROOT
from eti_pipeline.src.utilis.logger_utilis import setup_logging
from eti_pipeline.src.utilis.file_utilis import load_csv_safe



#Import
from config.config import(
    #File paths
    DATA_DIR,
    RAW_SUBDIR,
    RAW_FILENAME,

    #Output directories
    PROCESSED_SUBDIR,

    #Output filenames
    DEFAULT_OUTPUT_FILENAME,
    SUMMARY_FILENAME,

    #File formats
    DEFAULT_OUTPUT_FORMATS,

    #Pandas Save Parameters
    EXCEL_ENGINE,
    PARQUET_ENGINE,
    SAVE_INDEX,
    JSON_INDENT,
    JSON_ORIENT,
    CSV_LOW_MEMORY,

    #File encoding
    FILE_ENCODING,

    #Summary report settings
    SUMMARY_SEPARATOR,
    SUMMARY_SUBSEPARATOR,

    #File size calculation

    MB_CONVERSION,

    #log settings
    LOG_LEVEL,
    LOG_FORMAT

)

# Setup logger
logger = setup_logging(__name__)

from eti_pipeline.src.transform.transform import transform_fifa_data

def save_cleaned_data(raw_data, base_filename=DEFAULT_OUTPUT_FILENAME, formats=None):
    """Saves fifa cleaned data to multiple options."""

    if formats is None:
        formats=DEFAULT_OUTPUT_FORMATS

    # Use PROJECT_ROOT from utilities instead of manual path construction
    output_dir = os.path.join(PROJECT_ROOT, DATA_DIR, PROCESSED_SUBDIR)
    os.makedirs(output_dir, exist_ok=True)

    saved_files= {}

    logging.info(f"\n Saving cleaned data in {len(formats)} format(s)...")
    logging.info("=" * 50)

    #Save in each requested format

    for fmt in formats:
        filepath = os.path.join(output_dir, f"{base_filename}.{fmt}")

        try:
            if fmt == 'csv':
                raw_data.to_csv(filepath, index=SAVE_INDEX)
                logging.info(f" CSV saved:{filepath}")
            elif fmt == 'excel' or fmt == 'xlsx':
                raw_data.to_excel(filepath.replace('.excel','.xlsx'),index=SAVE_INDEX, engine=EXCEL_ENGINE)
                filepath = filepath.replace('.excel','.xlsx')
                logging.info(f" Excel saved:{filepath}")

            elif fmt == 'json':
                 raw_data.to_json(filepath, orient=JSON_ORIENT, indent= JSON_INDENT)
                 logging.info(f" JSON saved: {filepath}")

            elif fmt == 'parquet':
                raw_data.to_parquet(filepath, index=SAVE_INDEX, engine=PARQUET_ENGINE)
                logging.info(f" Parquet saved: {filepath}")

            elif fmt == 'feather':
                 raw_data.to_feather(filepath)
                 logging.info(f" Feather saved:{filepath}")
                
            elif fmt == 'pickle' or fmt == 'pkl':
                 raw_data.to_pickle(filepath.replace('.pickle','.pkl'))
                 filepath = filepath.replace('.pickle','.pkl')
                 logging.info(f"Pickled saved: {filepath}")
            else:
                 logging.info(f" Unknown format: {fmt}")
                 continue 
            saved_files[fmt]=filepath
        except Exception as e:
             logging.info(f"Error saving{fmt}: {str(e)}")
    logging.info(SUMMARY_SEPARATOR)
    logging.info(f"Saved {len(saved_files)} file(s) successfully!")
    logging.info(f"   Total size: {raw_data.shape[0]:,} rows × {raw_data.shape[1]} columns")
    
    return saved_files


def save_summary_statistics(raw_data, output_path=None):
    """Save a summary statistics report
    Args:
        df(pd.DataFrame): Cleaned Fifa data
        output_path (str): Where to save the summary
        """
    
    if output_path is None:
        output_path = os.path.join(PROJECT_ROOT, DATA_DIR, PROCESSED_SUBDIR, SUMMARY_FILENAME)


    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w',encoding=FILE_ENCODING) as f:
        f.write("Fifa 21 CLEANED DATA SUMMARY\n")
        f.write(SUMMARY_SEPARATOR + "\n\n")

        f.write(f"Dataset shape:{raw_data.shape[0]:,} rows * {raw_data.shape[1]} columns\n\n")

        f.write("COLUMN NAMES:\n")
        f.write(SUMMARY_SUBSEPARATOR * 60 + "\n")
        for i, col in enumerate(raw_data.columns, 1):
            f.write(f"{i:2d}.{col}\n")

        f.write("\n" + SUMMARY_SUBSEPARATOR + "\n")
        f.write("MISSING VALUES:\n")
        f.write(SUMMARY_SEPARATOR + "\n")
        missing = raw_data.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if len(missing) > 0:
            for col,count in missing.items():
                pct=(count / len(raw_data)) *100
                f.write(f"{col}: {count:,} ({pct:.2f}%)\n")

        else:
            f.write("No missing values")
        f.write("\n" + SUMMARY_SEPARATOR + "\n")
        f.write("DATA TYPES:\n")
        f.write(SUMMARY_SUBSEPARATOR + "\n")
        f.write(str(raw_data.dtypes))

    logging.info(f"Summary stats saved to: {output_path}")

#Testing the function

if __name__ == "__main__":

    logger.info("Testing save_data module")
    logger.info(SUMMARY_SEPARATOR)

    # Load raw data using the utility function
    file_location = os.path.join(PROJECT_ROOT, DATA_DIR, RAW_SUBDIR, RAW_FILENAME)
    raw_data = load_csv_safe(file_location, low_memory=CSV_LOW_MEMORY)

    if raw_data is not None:
        # Transform data
        cleaned_data = transform_fifa_data(raw_data)
        
        # Save CSV file only
        logger.info("\n Saving CSV file...")
        saved_files = save_cleaned_data(cleaned_data)
        
        # Save summary statistics
        save_summary_statistics(cleaned_data)
        
        logger.info("\n All files saved successfully!")
        logger.info("\nSaved files:")
        for fmt, path in saved_files.items():
            file_size = os.path.getsize(path) / MB_CONVERSION  # Convert to MB
            logger.info(f"  • {fmt.upper()}: {path} ({file_size:.2f} MB)")
    else:
        logger.error("Failed to load data!")
    

  

