import pandas as pd
import os
import re 


def convert_clause_thousands(values):
    """Converts Release clause to thousands in pounds"""
    #Input validation

    if not isinstance(values, str):
        return False 
    if '€' in values and not values.startswith('€'):
        return False 
    if values.count('€')>1:
        return False 
    clean_values=values.replace('€','').strip()
    if clean_values== '' or clean_values=='K' or clean_values=='M':
        return ''
    if clean_values.startswith('-'):
        return False 
    if clean_values.upper().count('K')>1:
        return False
    if clean_values.upper().startswith('K'):
        return False 
    if clean_values.upper().count('M')>1:
        return False 
    if clean_values.upper().startswith('M'):
        return False 
    
    if 'M' in clean_values:
        clean_digits=clean_values.replace('M','').strip()
        try:
            clean_release_column=float(clean_digits)*1000000
            if clean_release_column>203100000.0:
                return False 
            return clean_release_column
        except ValueError:
            return False 
    
    elif 'K' in clean_values:
        clean_digits=clean_values.replace('K','').strip()
        try:
            clean_release_column= float(clean_digits)*1000
            if clean_release_column>203100000.0:
                return False 
            return clean_release_column
        except ValueError:
            return False 
    else:
        return 0.0
        
