import pandas as pd
import numpy as np
import os
import re

def convert_hits_column(values):
    """Convert hits column to numeric formart"""
    #Input Validation

    if pd.isna(values):
        return 0.0
    values=values.upper().strip()
    if values.startswith('-'):
        return False 
    if 'K' in values and not values.endswith('K'):
        return False 
    if values.upper().count('K')>1:
        return False
    if values.count('.')>1:
        return False 
    if ';' in values or ':' in values:
        return False 
    if values=='' or values=='K':
        return ''
    
    clean_values=values.upper().strip()
    #Check if K exists

    if 'K' in clean_values:
        clean_digits=clean_values.replace('K','').strip()
        clean_values=float(clean_digits) * 1000
        return clean_values
    else:
        clean_digits=float(clean_values)
        return clean_digits 