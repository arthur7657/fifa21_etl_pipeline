import sys
import pytest
from pathlib import Path


#Adding project root to path

sys.path.insert(0,str(Path(__file__).parent.parent))

from eti_pipeline.src.transform.string_converter_value import convert_value_column 
from eti_pipeline.src.transform.string_converter_weight import convert_weight_column 
from eti_pipeline.src.transform.string_converter_height import convert_height_column 
from eti_pipeline.src.transform.string_converter_wages import convert_wages_thousands
from eti_pipeline.src.transform.string_converter_clause import convert_clause_thousands
from eti_pipeline.src.transform.string_converter_hits import convert_hits_column        



#Tests the cleaning/transform logic

class TestConvertHeight:
    """All tests for convert_height_column"""

    #Boundaries
    
    def test_height_boundaries(self):
        assert convert_height_column('0')== False 
        assert convert_height_column('195CM')==195.0
        assert convert_height_column('-10cm')== False
        assert convert_height_column('226cm')== False 

    #Ordinary

    def test_height_ordinary(self):
        assert convert_height_column('100cm')== 100.0
        assert convert_height_column('183cm')== 183.0
        assert convert_height_column("5'10")== 177.8
        assert convert_height_column("6'3")== 190.5

    #Malformed

    def test_height_malformed(self):
        assert convert_height_column('cm100')== False
        assert convert_height_column('cmcm100')== False 
        assert convert_height_column('100cmcm')== False 
        assert convert_height_column('100:1cm')== False 

    #Blank/Nulls

    def test_height_blanks(self):
        assert convert_height_column("")==""
        assert convert_height_column("  ")==""
        assert convert_height_column("cm")==""
        assert convert_height_column('0cm')== False 
        assert convert_height_column(None) == 0.0 

    #Extreme

    def test_height_extreme(self):
        assert convert_height_column('00000')== False 
        assert convert_height_column('226cm')== False
    

    #Character/Content Count

    def test_height_char(self):
        assert convert_height_column("  200cm  ")== 200.0
        assert convert_height_column("200cm   ")== 200.0
        assert convert_height_column("  200cm")== 200.0
        assert convert_height_column("  200cm  ")==200.0
    

class TestConvertWeight:
    """All tests for convert_weight_column"""
    pass 


class TestConvertValue:
    """All tests for convert_value_column"""
    pass


class TestConvertWagesThousands:
    """All tests for convert_wages_thousands function"""

    #Boundaries

    def test_wages_boundaries(self):
        """Tests the lowest and highest value in the wages column"""
        assert convert_wages_thousands('€0')==0.0
        assert convert_wages_thousands('€560K')==560.0
        assert convert_wages_thousands('€-100K')==False
        assert convert_wages_thousands('€100000k')==False

    #Ordinary

    def test_wages_ordinary(self):
        """Tests the common valid and common invalid values in the wages column"""
        #Tests for common valid values
        assert convert_wages_thousands('€200K')==200.0
        assert convert_wages_thousands('€125K')==125.0
        assert convert_wages_thousands('€1K')==1.0
        assert convert_wages_thousands('€0')==0.0
        assert convert_wages_thousands('€500')==0.5
        assert convert_wages_thousands('€1000')==1.0

        #Tests for invalid values
        assert convert_wages_thousands('€ABCK')==False
        assert convert_wages_thousands('500')==0.5

    #Tests for Malinformed

    def test_wages_malformed_cases(self):
        """Tests malformed cases in the wages column"""
        assert convert_wages_thousands('500K')==500.0
        assert convert_wages_thousands('500€K')==False 
        assert convert_wages_thousands('K€500')==False
        assert convert_wages_thousands('€€200K')==False
        assert convert_wages_thousands('€200KK')==False 
        assert convert_wages_thousands('€K200')==False
        assert convert_wages_thousands('K200€')==False 


    #Tests for Blank Nulls

    def test_wages_blank_null(self):
        """Tests the blank nulls in the wages column"""
        assert convert_wages_thousands("")==''
        assert convert_wages_thousands("   ")==''
        assert convert_wages_thousands('€')==''
        assert convert_wages_thousands('€K')==''

    #Tests Extremes

    def test_wages_extreme_cases(self):
        """Tests extreme cases in the wages column"""
        assert convert_wages_thousands('€00000K')==0.0
        assert convert_wages_thousands('€0K')==0.0
        assert convert_wages_thousands('1K')==1.0
        assert convert_wages_thousands('€559K')==559.0
        assert convert_wages_thousands('€0')==0.0

class Testconvert_clause_thousands:
    """All tests for convert_clause_thousands"""
    #Boundaries

    def test_clause_boundaries(self):
        assert convert_clause_thousands('€0')==0.0
        assert convert_clause_thousands('€203.1M')==203100000.0
        assert convert_clause_thousands('€-1M')== False
        assert convert_clause_thousands('€500M')==False 

    #Ordinary

    def test_clause_ordinary(self):
        assert convert_clause_thousands('€138.4M')==138400000.0
        assert convert_clause_thousands('€20.1M')==20100000.0
        assert convert_clause_thousands('€71K')==71000
        assert convert_clause_thousands('€0')==0.0

    #Malformed

    def test_clause_malformed(self):
        assert convert_clause_thousands('138.4M')==138400000.0
        assert convert_clause_thousands('138.4€M')==False
        assert convert_clause_thousands('€M138.4')==False 
        assert convert_clause_thousands('138.4€M')==False 
        assert convert_clause_thousands('138.4€€')==False 
        assert convert_clause_thousands('€€138.4K')==False 
        assert convert_clause_thousands('€138.4MM')==False
        assert convert_clause_thousands('M138.4K')==False 


    #Blank/Null

    def test_clause_blank(self):
        assert convert_clause_thousands('')==''
        assert convert_clause_thousands('   ')==''
        assert convert_clause_thousands('€')==''
        assert convert_clause_thousands('€K')==''

    #Tests Extreme

    def test_clause_extreme(self):
        assert convert_clause_thousands('€00000')==0.0
        assert convert_clause_thousands('€0M')==0.0
        assert convert_clause_thousands('€0K')==0.0
        assert convert_clause_thousands('€203M')==203000000.0
        assert convert_clause_thousands('€0')==0.0

class Testconvert_hits_column:
    """All tests related to the Hits column"""
    #Boundaries
    def test_hits_boundaries(self):
        assert convert_hits_column('0')==0.0
        assert convert_hits_column('4K')==4000.0
        assert convert_hits_column('-1')==False
        assert convert_hits_column('10K')==10000.0


    #Ordinary
    def test_hits_ordinary(self):
        assert convert_hits_column('10')==10.0
        assert convert_hits_column('11.0')==11.0
        assert convert_hits_column('1.2K')==1200.0
        assert convert_hits_column('3K')==3000.0

    #Malformed
    def test_hits_malformed(self):
        assert convert_hits_column('1.2')==1.2
        assert convert_hits_column('K1.2')==False
        assert convert_hits_column('KK1.2')==False
        assert convert_hits_column('1:2')==False
        assert convert_hits_column('1:2:0')==False
        assert convert_hits_column('1.2.0')==False 
        assert convert_hits_column('1.3KK')==False 



    #Blanks
    def test_hits_blanks(self):
        assert convert_hits_column("")==""
        assert convert_hits_column("     ")==""
        assert convert_hits_column("K")==''

    


    #Extreme
    def test_hits_extreme(self):
        assert convert_hits_column('0000000')==0.0
        assert convert_hits_column('1.2K')==1200.0
        assert convert_hits_column('0')==0.0
        assert convert_hits_column('10K')==10000.0
        



    


    
        

                                       
                                       

