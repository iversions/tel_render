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


def mtnlext (path):
#path = r'D:\TELEPHONE_BILLS\MTNL.pdf'
    with pdfplumber.open(path) as p0:
        firstpage = p0.pages[0]
        charst = firstpage.extract_words()
        
    # im = firstpage.to_image(resolution=300)
    # im.draw_rects(firstpage.extract_words())
    #box2 = (40,20,280,90)
    #box3 = (20,230,280,300)
    #box4 = (20,50,250,170)
    # invc1 = firstpage.within_bbox(box2)
    #invc1 = firstpage.within_bbox(box2)
    #invc3 = invc1.extract_text()
    invc3 = firstpage.extract_table()
    #print('\n')
    #print(invc3)
    #print(U+FFFD)

    #x = 0
    #for q in z:
        #print(f'{x},{z[x]}')
    #    x+=1




    training_params = []
    u = 0
    z = []
    for x in charst:
        w = charst[u]['text']
        #print(f'Charset {y} is:',w)
        u+=1
        #print('\n')
        z.append(w)
    K =':'
    while(K in z):
        z.remove(K)    
    #print('List is', z)
    #print(charst[0]['text'])    
    #print('List is:',z)


    e = 0
    for w in z:
        #print(o,'   ',z[p:p+2])
        if  z[e] == 'Name:':
            #print('Bill Period is:', z[p+2:])
            aaa = z[e+1:]
            name1 = 0
            yyy = []
            for aa in aaa:
                if aaa[name1] == 'Installation':
                    cc = name1
                    employee_name = " ".join(str(i) for i in aaa[:cc])
                    
                name1+=1
            break
        if (e+2)<= len(z):
            e+=1





    o = 0
    for w in z:
        #print(o,'   ',z[o:o+2])
        #print(o,'  ',z[o])
        if " ".join(str(i) for i in  z[o:o+2]) == 'Amount Payable':
            aaa = o
            break
        if (o+2)<= len(z):
            o+=1
    
    bill_no = z[o+3]
    print('Bill No is:', bill_no)
    print('\n')
    bill_period_from = z[o+13]
    bill_period_to = z[o+15] 
    print('Bill Period is:',bill_period_from, 'to' ,bill_period_to)
    print('\n')
    bill_date =z[o+16]
    print('Bill Date is:', bill_date)
    print('\n')
    telephone_no = z[o+12]
    print('Telephone Number is:', telephone_no)




    print('\n')




    r = 0
    for w in z:
        #print(r,'   ',z[r:r+2])
        if " ".join(str(i) for i in  z[r:r+3]) == 'Total Taxable Value':
            bill_amount = z[r+3]
            print('Bill Amount is:', bill_amount)
            aaa = z[r+2]
        if (r+2)<= len(z):
            r+=1





    print('\n')







    t = 0
    for w in z:
        #print(r,'   ',z[r:r+2])
        if " ".join(str(i) for i in  z[t:t+3]) == 'CGST @ 9%':
            cgst = z[t+3]
            sgst = z[t+3]
            print('CGST is:',cgst )
            print('SGST is:',sgst )
            aaa = z[t+2]
        if (t+2)<= len(z):
            t+=1



    t = 0
    for w in z:
        #print(r,'   ',z[r:r+2])
        if " ".join(z[t:t+4]) == 'Other Non Taxable Credit':
            non_taxable = z[t+4]
            break
        t+=1

    t = 0
    for w in z:
        #print(r,'   ',z[r:r+2])
        if " ".join(z[t:t+3]) == 'Total Taxable Value':
            taxable = z[t+3]
            break
        t+=1

    print('\n')
    total_amount = z[o+5]
    print('Total Amount is:', total_amount)



    print('Employee Name is :', employee_name)

    print(non_taxable)

    ship_to_state_code,supply = '-','-'
    taxes = '-'

    duplicate = duplicate_bill_check(bill_no)

    if duplicate == 1:
        status = 'DUPLICATE'
    if duplicate ==  0:
        status = 'PROCCESSED'

    insert_into_main_table('MTNL',status,employee_name,bill_no,bill_period_from,bill_period_to,bill_date,telephone_no,bill_amount,cgst,sgst,total_amount,path,taxes,taxable,non_taxable,ship_to_state_code,supply)







