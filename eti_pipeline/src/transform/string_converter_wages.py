import pandas as pd
import os
import re

def convert_wages_thousands(values):
        """Converts strings to floats in the wage column"""
        #Remove '€' symbol from the string

        if not isinstance(values, str):
             return False
        
        if '€' in values and not values.startswith('€'):
             return False
        if values.count('€') > 1:
             return False 
        
        clean_value= values.replace('€','').strip()
        
        #Handle empty

        if clean_value=='' or clean_value== 'K':
             return ''
        
        #Check for negative values

        if clean_value.startswith('-'):
             return False


        #Remove 'K' and divide where necessary.

        if clean_value.upper().count('K') > 1:
             return False
        
        if clean_value.upper().startswith('K'):
             return False

    
        if 'K'in clean_value.upper():
            clean_str=clean_value.upper().replace('K','').strip()
            try:
                 clean_wage_column=float(clean_str)
                 if clean_wage_column > 560.0:
                      return False
                 return clean_wage_column
            except ValueError:
                 return False
            

        else:
            try:
                 clean_str=clean_value.strip()
                 convert_float=float(clean_str)
                 clean_wage_column=convert_float / 1000
                 if clean_wage_column >560.0:
                      return False
                 return clean_wage_column
            except ValueError:
                 return False
            

            