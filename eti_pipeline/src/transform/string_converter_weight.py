import pandas as pd
import os
import re 



def convert_weight_column(values):
    """Converts the weight column from a string to an integer in a standerdized formart"""
    
    #Handle None/empty cases

    if values is None:
        return None 
    
    if values == "":
        return None 
    
    #Prepare string for processing

    cleaned= str(values).upper().strip()

    #Check if empty after stripping

    if cleaned == "":
        return None 
    
    #Validate format(has 'kg' suffic)

    if not cleaned.endswith('KG') and not cleaned.endswith('LBS'):

        return None 
    

    
    #Extract numeric part
    

    if cleaned.endswith('KG'):
        numeric_str=cleaned.removesuffix('KG')
        try:
            
            weight_KG=float(numeric_str)
        except ValueError:
            return None 
        
    elif cleaned.endswith('IBS'):
        numeric_str=cleaned.removesuffix('IBS')
        try:
            weight_lbs=float(numeric_str)
            weight_KG=weight_lbs/2.20462
        except ValueError:
            return None 
        
    else:
        return None 
    

    #Validate range
    if weight_KG <50 or weight_KG > 150:
        return None 
    
    return weight_KG
    
            

#======Quick component tests=====

#Testing None/empty

#print("Testing None/Empty:")
###print(f"'' -{convert_weight_column('')}")
#print(f"'  '-{convert_weight_column('')}")
#print()

#Test valid cases

#print("Testing Valid:")
#print(f"'110kg'- {convert_weight_column('110kg')}")
#print(f"' 75KG'- {convert_weight_column(' 75KG ')}")
#print(f"'50kg' - {convert_weight_column('50kg')}")
#print()

#Test malformed

#print("Testing malformed")
#print(f"'kgkg'- {convert_weight_column('kgkg')}")
#print(f"'110kg'- {convert_weight_column('110kg')}")
#print(f"'kg110'- {convert_weight_column('kg110')}")
#print()

#Test boundaries

#print("Test Boundaries")
#print(f"'49kg'- {convert_weight_column('49kg')}")
#print(f"'151kg'-{convert_weight_column('151kg')}")
#print(f"'150kg'-{convert_weight_column('150kg')}")
#print()

