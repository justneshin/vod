import random
import sys
import copy

visaPrefixList = [  ['4', '5', '3', '9'], 
                    ['4', '5', '5', '6'], 
                    ['4', '9', '1', '6'],
                    ['4', '5', '3', '2'], 
                    ['4', '9', '2', '9'],
                    ['4', '0', '2', '4', '0', '0', '7', '1'],
                    ['4', '4', '8', '6'],
                    ['4', '7', '1', '6'],
                    ['4'] ]

mastercardPrefixList = [    ['5', '1'],
                            ['5', '2'],
                            ['5', '3'],
                            ['5', '4'],
                            ['5', '5'] ]
"""
'prefix' is the start of the CC number as a string, any number of digits.
'length' is the length of the CC number to generate. Typically 13 or 16
"""
def completed_number(prefix, length):

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
    	digit = random.choice(['0',  '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    	ccnumber.append(digit)


    # Calculate sum 

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:

        odd = int( reversedCCnumber[pos] ) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):

            sum += int( reversedCCnumber[pos+1] )

        pos += 2

    # Calculate check digit

    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10

    ccnumber.append( str(checkdigit) )
    
    return ''.join(ccnumber)

def credit_card_number(prefixList, length, howMany):
    result = []
    
    for i in range(howMany):
        
        ccnumber = copy.copy(random.choice(prefixList) )
        
        result.append( completed_number(ccnumber, length) )
    
    return result

def output(title, numbers):

    result = []
    result.append(title)
    result.append( '-' * len(title) )
    result.append( '\n'.join(numbers) )
    result.append( '' )

    return '\n'.join(result)
