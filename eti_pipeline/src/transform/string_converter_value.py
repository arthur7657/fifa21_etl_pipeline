import pandas as pd
import os
import re 


def convert_value_column(values):
    """Converts the value string column into an standardized integer"""
    #Handle None and empty cases

    if values is None or values =="":
        return None 
    values=str(values)
    values=values.strip()

    if values == "":
        return None 
    
    #Prepare the string/Normalize the string

    values=values.upper()
    values=values.strip()

    #Handle special cases here
    if values == "€0K" or values =="€0M":
        return None 
    
    #Validate format: Must start with '€'
    if not values.startswith('€'):
        return None 
    
    #Extract currency symbol
    values=values.removeprefix('€')
    values=values.strip()

    #Check if the remaining string value is empty
    if values == '':
        return None 
    
    #Validate:Should not start with M or K(malformed)
    if values.startswith('M') or values.startswith('K'):
        return None 
    
    #Determine multiplied and extract base number
    if values.endswith('M'):
        values=values.removesuffix('M')
        values=values.strip()
        try:
            base_number= float(values)
            clean_value= base_number * 1_000_000
        except ValueError:
            return None 
    elif values.endswith('K'):
        values=values.removesuffix('K')
        values= values.strip()
        try:
            base_number = float (values)
            clean_value = base_number * 1_000
        except ValueError:
            return None 
    else:
        values=values.strip()
        try:
            base_number = float(values)
            clean_value = base_number * 1
        except ValueError:
            return None 
    
    #Validate range
    if clean_value < 0 or clean_value >200_000_000:
        return None 
    return clean_value 
    

#=====Quick Component Testing====

if __name__ == "__main__":
    print('='*60)
    print('COMPONENT TESTS: convert_value_column')
    print('='*60)

    #Testing none and empty cases

    print('Testing None/Empty:')

    result = convert_value_column('')
    expected = None 
    print(f"''→ {result} (expected: {expected}) {'✓' if result == expected else '❌'}")

    result = convert_value_column('None')
    expected = None 
    print(f"None → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")

    result = convert_value_column('  ')
    expected = None 
    print(f"'  ' → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")
    

    #Testing valid M suffix

    print('Testing Valid M Suffix')

    print("\n [Test 2] Valid M Suffix")
    result = convert_value_column ('€100M')
    expected = 100_000_000.0
    print(f"'€100M'  → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")
    

    result = convert_value_column('€1.5M')
    expected = 1_500_000
    print(f"'€1.5M'    → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")
    

    result = convert_value_column(' €50M ')
    expected = 50_000_000.0
    print(f" ' €50M ' → {result} (expected) :{expected}) {'✓' if result == expected else '❌'}")

    #Testing Valid  K suffix

    print('\n [Test 3] Valid K')

    result = convert_value_column('€100K')
    expected = 100_000.0
    print(f"'€100K' → {result} (expected) :{expected}) {'✓' if result == expected else '❌'}")

    result = convert_value_column('€50K')
    expected = 50_000.0
    print(f"'€50K' → {result} (expected) :{expected}) {'✓' if result == expected else '❌'}")
    

    #No suffix

    print('\n[Test 4] No Suffix')

    result = convert_value_column('€100')
    expected = 100.0
    print(f"'€100' → {result} (expected) :{expected}) {'✓' if result == expected else '❌'}")
    

    result = convert_value_column('€50.5')
    expected = 50.5
    print(f"'€50.5' → {result} (expected) :{expected}) {'✓' if result == expected else '❌'}")
    

    #Special case

    print('\n[Test 5] Special Case:')
    result = convert_value_column('€0K')
    expected = None 
    print(f"'€0K' → {result} (expected) :{expected}) {'✓' if result == expected else '❌'}")
    

    result = convert_value_column('€0M')
    expected = None 
    print(f"'€0M' → {result} (expected) :{expected}) {'✓' if result == expected else '❌'}")
    


  
    # Test 6: Malformed
    print('\n[Test 6] Malformed:')
    result = convert_value_column('€M100')
    expected = None
    print(f"'€M100' → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")
    
    result = convert_value_column('€K50')
    expected = None
    print(f"'€K50'  → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")
    
    result = convert_value_column('100M')
    expected = None
    print(f"'100M'  → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")
    
    result = convert_value_column('€abc')
    expected = None
    print(f"'€abc'  → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")
    
    result = convert_value_column('€')
    expected = None
    print(f"'€'     → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")
    
    # Test 7: Boundaries
    print('\n[Test 7] Boundaries:')
    result = convert_value_column('€1M')
    expected = 1_000_000.0
    print(f"'€1M'   → {result} (expected: {expected}) {'✓' if result == expected else '❌ BUG 2'}")
    
    result = convert_value_column('€200M')
    expected = 200_000_000.0
    print(f"'€200M' → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")
    
    result = convert_value_column('€201M')
    expected = None
    print(f"'€201M' → {result} (expected: {expected}) {'✓' if result == expected else '❌ BUG 3'}")
    
    result = convert_value_column('€-10M')
    expected = None
    print(f"'€-10M' → {result} (expected: {expected}) {'✓' if result == expected else '❌'}")

    print('\n' + '='*60)





