import pandas as pd
import os
import re

def convert_height_column(values):
    """Converting height column from a string to an integer"""

    #Input validation
    
    #Handle null values
    if pd.isna(values):
        return 0.0
    
    #Convert string and clean

    values=str(values).strip()

    #Handle empty strings
    if values == '' or values == 'cm':
        return ''
    
    #Uppercase
    clean_values= values.upper()

    #check for feets and inches

    if "'" in clean_values:
        #Use regex to extract numbers
        match = re.match(r"(\d+)'(\d+)", clean_values)
        if match:
            feet = float(match.group(1))
            inches = float(match.group(2))
            total_inches = (feet * 12) + inches 
            converted_cm = round(total_inches * 2.54,2)
            return converted_cm 
        
        else:
            return False 
    
    elif 'CM' in clean_values:
        #Validation:'cm' should not appear more than once 

        if clean_values.count('CM')>1:
            return False 
        if clean_values.startswith('CM'):
            return False 
        
        try:
            remove_cm = clean_values.replace('CM','').strip()
            converted_cm = float(remove_cm)

            if converted_cm <= 0 or converted_cm > 220:
                return False 
            
            return converted_cm 
        except ValueError:
            return False 
    else:
        
        try:
            converted_cm = float(clean_values)
            if converted_cm <= 0 or converted_cm >220:
                return False 
            return converted_cm
        except ValueError:
            return False 
        
    

# Test the function when running this file directly
if __name__ == "__main__":
    print("Testing convert_height_column function:")
    print("=" * 50)
    
    test_cases = [
        "180cm",      # Should work
        "180",        # Should work now!
        "5'10",       # Should work
        "CM180",      # Should return False
        "abc",        # Should return False
        "",           # Should return ''
        "195CM",      # Should work
        "6'3",        # Should work
        None,         # Should return 0.0
    ]
    
    for test in test_cases:
        result = convert_height_column(test)
        print(f"  '{test}' → {result}")
        



