import os
import sys
import pandas as pd
import logging

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from eti_pipeline.src.utilis.path_utilis import PROJECT_ROOT
from config.config import DATA_DIR, CSV_LOW_MEMORY

def load_csv_safe(file_path: str, **kwargs) -> pd.DataFrame:
    """Safely load CSV with comprehensive error handling.
    
    Raises explicit exceptions instead of returning None.
    Provides helpful error messages for debugging.

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file can't be read
        pd.errors.EmptyDataError: If file is empty or has no data
        pd.errors.ParserError: If CSV is malformed
        UnicodeDecodeError: If file encoding is wrong
    
    """

    # Check 1: Does the file exists


    if not os.path.exists(file_path):
        #Get directory  (handle case where it's  just a file)
        file_dir = os.path.dirname(file_path)
        if not file_dir:
            file_dir = os.getcwd()
        error_msg = (
            f"\n FILE NOT FOUND: {os.path.basename(file_path)}\n"
            f" EXPECTED LOCATION: {os.path.dirname(file_path)}\n"
            f" Full path: {file_path}\n"
            f"\n  Please check:\n"
            f"  1. File exists in the correct folder\n"
            f"  2. File name spelling is correct\n"
            f"  3. File extension is .csv"
        )
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    # Check 2: Is it readable
    
    if not os.access(file_path, os.R_OK):
        error_msg = f" CANNOT READ FILE(permission denied):{file_path}"
        logging.error(error_msg)
        raise PermissionError(error_msg)
    
    #Check 3: If file is empty
    if os.path.getsize(file_path) == 0:
        error_msg = f"❌ File is empty (0 bytes): {os.path.basename(file_path)}"
        logging.error(error_msg)
        raise pd.errors.EmptyDataError(error_msg)
    

    #Try to load CSV

    try:
        logging.info(f"Loading CSV: {os.path.basename(file_path)}")
        df = pd.read_csv(file_path, **kwargs)
        
        # Check 4: Did we actually get data?
        if df.empty or len(df) == 0:
            error_msg = f"❌ CSV loaded but contains 0 data rows: {os.path.basename(file_path)}"
            logging.error(error_msg)
            raise pd.errors.EmptyDataError(error_msg)
        
        logging.info(f"✅ Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")
        return df
        
    except pd.errors.EmptyDataError as e:
        # Could be from pandas OR our check above
        # Re-raise with our message if it's pandas' generic message
        if "No columns to parse" in str(e):
            error_msg = f"❌ CSV file is empty or has no valid data: {os.path.basename(file_path)}"
            logging.error(error_msg)
            raise pd.errors.EmptyDataError(error_msg) from e
        else:
            # It's our custom message, just re-raise
            raise
        
    except pd.errors.ParserError as e:
        error_msg = (
            f"\n CSV file is corrupted or malformed: {file_path}\n"
            f"   Parser error: {str(e)}\n"
            f"   This usually means:\n"
            f"   - File is not actually a CSV\n"
            f"   - CSV has inconsistent number of columns\n"
            f"   - File encoding is wrong"
        )
        logging.error(error_msg)
        raise pd.errors.ParserError(error_msg) from e
    
    except UnicodeDecodeError as e:
        error_msg = (
            f"\n Cannot read file encoding: {file_path}\n"
            f"   Error: {str(e)}\n"
            f"   Try adding encoding='utf-8' or encoding='latin-1'"
        )
        logging.error(error_msg)
        raise UnicodeDecodeError(e.encoding, e.object, e.start, e.end, error_msg) from e
    
    except Exception as e:
        error_msg = f" Unexpected error loading CSV: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg) from e

# Test code
if __name__ == "__main__":
    from logger_utilis import setup_logging
    
    # Setup logging
    logger = setup_logging(__name__)
    
    print("=" * 50)
    print("Testing file_utilis.py")
    print("=" * 50)
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"DATA_DIR: {DATA_DIR}")
    print()
    
    # Test 1: Missing file (should fail gracefully)
    print("TEST 1: Loading non-existent file...")
    print("-" * 50)
    try:
        result = load_csv_safe("nonexistent.csv", low_memory=CSV_LOW_MEMORY)
        print("❌ TEST FAILED - Should have raised FileNotFoundError!")
    except FileNotFoundError as e:
        print("✅ TEST PASSED - FileNotFoundError raised correctly!")
        print(f"   Error message starts with: {str(e)[:50]}...")
    
    print()
    
    # Test 2: Try loading actual FIFA CSV (if it exists)
    print("TEST 2: Loading actual FIFA CSV...")
    print("-" * 50)
    fifa_path = os.path.join(PROJECT_ROOT, DATA_DIR, "raw", "fifa21 raw data v2.csv")
    
    if os.path.exists(fifa_path):
        try:
            result = load_csv_safe(fifa_path, low_memory=CSV_LOW_MEMORY)
            if result is not None and not result.empty:
                print(f"✅ TEST PASSED - Loaded {len(result):,} rows successfully!")
            else:
                print("⚠️  WARNING - File loaded but DataFrame is empty")
        except Exception as e:
            print(f"❌ TEST FAILED - Unexpected error: {e}")
    else:
        print(f"⚠️  SKIPPED - FIFA CSV not found at: {fifa_path}")
    
    print()
    print("=" * 50)
    print("✅ file_utilis.py testing complete!")
    print("=" * 50)


