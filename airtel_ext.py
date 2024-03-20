import os
import glob
import pdfplumber
# import pandas as pd
# from tabulate import tabulate
import re
from string import ascii_lowercase
from itertools import groupby
from tel_int import insert_into_main_table
from tel_int import duplicate_bill_check
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

all_text = []
words = []
print('Waiting')
#path = 'D:\TELEPHONE_BILLS\Airtel_UAT_1.pdf'

def airext (path):
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_words = page.extract_words()
            words.extend([word['text'] for word in page_words])

    all_text = []
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split('\n')
        all_text.extend(lines)


    try:
        for line in all_text:
            if "Billing Address" in line:
                employee_name = all_text[all_text.index("Billing Address") + 1]
        print(employee_name)
    except Exception as e:
        employee_name ='-'
    
    
    try:
        a = 0
        for word in words:
            if ' '.join(words[a:a+4]) == 'Ship To State Code':
                ship_to_state_code = words[a+5]
                break
            a+=1
        print(ship_to_state_code)
    except Exception as e:
        ship_to_state_code ='-'
    try:
        a = 0
        for word in words:
            if ' '.join(words[a:a+2]) == 'Bill NO':
                bill_no = words[a+2]
                break
            a+=1
        print(bill_no)
    except Exception as e:
        bill_no ='-'
    
    try:
        a = 0
        for word in words:
            if ' '.join(words[a:a+2]) == 'Bill Period':
                bill_period_from = ' '.join(words[a+2:a+7]).split('-')[0]
                bill_period_to = ' '.join(words[a+2:a+7]).split('-')[1]
                break
            a+=1
        print(bill_period_from,bill_period_to)
    except Exception as e:
        try:
            a = 0
            for word in words:
                if ' '.join(words[a:a+2]) == 'Bill Period':
                    bill_period_from = ' '.join(words[a+2:a+9]).split('to')[0]
                    bill_period_to = ' '.join(words[a+2:a+9]).split('to')[1]
                    break
                a+=1
            print(bill_period_from,bill_period_to)
        except Exception as e:
            bill_period_from='-'
            bill_period_to ='-'
    
    try:
        a = 0
        for word in words:
            if ' '.join(words[a:a+2]) == 'Bill Date':
                bill_date = ' '.join(words[a+2:a+5])
                break
            a+=1
        print(bill_date)
    except Exception as e:
        bill_date ='-'
    
    try:
        a = 0
        for word in words:
            if ' '.join(words[a:a+2]) == 'Rental Charges':
                bill_amount = words[a+2]
                break
            a+=1
        print(bill_amount)
    except Exception as e:
        bill_amount ='-'
    
    try:
        a = 0
        for word in words:
            if words[a] == 'Taxes' and ' '.join(words[a+2:(a+4)]) == 'Total Amount':
                taxes = words[a+1]
                total_amount = words[a+5]
                break
            a+=1
        print(taxes,total_amount)
    except Exception as e:
        taxes ='-'
        total_amount ='-'
    
    
    try:
        for line in all_text:
            if 'PhoneNo' in line:
                telephone_no = line.split(':')[1]
        print('>>> ',telephone_no)
    except Exception as e:
        telephone_no ='-'
    
    try:
        a = 0
        for word in words:
            if ' '.join(words[a:a+4]) == 'Place of Supply :':
                supply = words[a+4]
                break
            a+=1
        print(supply)
    except Exception as e:
        supply = '-'
    cgst ='-'
    sgst ='-'
    taxable ='-'
    non_taxable ='-'

    duplicate = duplicate_bill_check(bill_no)

    if duplicate == 1:
        status = 'DUPLICATE'
    if duplicate ==  0:
        status = 'PROCCESSED'

    
    insert_into_main_table('AIRTEL',status,employee_name,bill_no,bill_period_from,bill_period_to,bill_date,telephone_no,bill_amount,cgst,sgst,total_amount,path,taxes,taxable,non_taxable,ship_to_state_code,supply)


