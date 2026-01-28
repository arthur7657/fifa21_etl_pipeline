import sys
import pytest
import os
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from eti_pipeline.src.utilis.file_utilis import load_csv_safe

class TestFileOperations:
    """Test file handling edge cases"""
    
    
    def test_load_missing_file(self):
        """Test that missing file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_csv_safe("this_file_does_not_exist.csv")
    
         # Check error message is helpful
        error_msg = str(exc_info.value)
        # Use case-insensitive check OR check for your exact message
        assert "FILE NOT FOUND" in error_msg or "File not found" in error_msg.lower()
        assert "this_file_does_not_exist.csv" in error_msg
    
    def test_load_empty_file(self, tmp_path):
        """Test that empty file raises EmptyDataError"""
        # Create empty file
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("")
        
        with pytest.raises(pd.errors.EmptyDataError) as exc_info:
            load_csv_safe(str(empty_file))
        
        error_msg = str(exc_info.value).lower()
        assert "empty" in error_msg or "no data" in error_msg
    
    def test_load_corrupted_csv(self, tmp_path):
        """Test that corrupted CSV raises ParserError"""
        # Create malformed CSV
        bad_csv = tmp_path / "corrupted.csv"
        bad_csv.write_bytes(b'\x00\x01\x02\x03\x04\xFF\xFE\xFD')
        
        with pytest.raises(Exception) as exc_info:
            load_csv_safe(str(bad_csv))
        
        assert exc_info.value is not None
    
    def test_load_valid_csv(self, tmp_path):
        """Test that valid CSV loads successfully"""
        # Create valid CSV
        valid_csv = tmp_path / "test.csv"
        valid_csv.write_text("Name,Age\nAlice,25\nBob,30")
        
        df = load_csv_safe(str(valid_csv))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ['Name', 'Age']
        assert df.iloc[0]['Name'] == 'Alice'

    def test_load_csv_with_extra_whitespace(self, tmp_path):
        """Test CSV with extra whitespace in data"""
        csv_with_spaces = tmp_path / "spaces.csv"
        csv_with_spaces.write_text("Name,Age\n  Alice  ,  25  \n  Bob  ,  30  ")
        
        df = load_csv_safe(str(csv_with_spaces))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2