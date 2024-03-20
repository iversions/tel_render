import re
import pdfplumber
from Air_int import insert_into_main_table
from Air_int import duplicate_bill_check
def airinvex(path):
    with pdfplumber.open(path) as pdf:
        pg = pdf.pages[0]
        extracted_text = pg.extract_text()
        table = pg.extract_table()
        
    pgnr_nm= '-';inv_no= '-';inv_dte= '-';flghfrom= '-';flght_to= '-';sac= '-';tax_val= '-';nontax_val= '-';tot= '-';igst_amt= '-';cgst_amt='-';sgst_amt='-';tot_inval = '-';

    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    def dictionarymaker(row):
        return {columns[i]:datacheck(i,cell) for i, cell in enumerate(row)}
    def datacheck(j,i):
        if i is None: return None
        if i==0: return 0
        if i=="": return None
        if "\n" in i:return i.replace("\n","").replace(",","")
        if "," in i: return i.replace(",","")
        return i
    def split1(j):
        if '' or "\n" not in j:
            return j,''
        if "\n" in j:
            temp = j.split("\n")
            return temp[0],temp[1]
        if '' in j:
            return '',''

    gstin_regex = r'[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}'
    gstin_number = re.findall(gstin_regex, extracted_text)

    sup_gst = gstin_number[0]
    cus_gst = gstin_number[1]
    for i in extracted_text.split("\n")[0:15]:
        if 'AirAsia' in i:
            for row in extracted_text.split("\n"):
                try:
                    if "Passenger Name :" in row: pgnr_nm = row.split("Passenger Name : ")[-1] 
                    print(pgnr_nm)  
                except Exception as e:
                    pgnr_nm = ''
                try:
                    if "Invoice Number :" in row: inv_no = row.split("Invoice Number : ")[-1]
                    print(inv_no)
                except Exception as e:
                    inv_no =''
                try:
                    if "Invoice Date :" in row: inv_dte = row.split("Invoice Date : ")[-1]
                    print(inv_dte)
                except Exception as e:
                    inv_dte = ''
                try:
                    if "GSTN :" in row: gstn = row.split("GSTN : ")[-1]
                except Exception as e:
                    gstn =''
                try:
                    if "Flight From : " in row: flghfrom = row.split("Flight From : ")[1].split()[0]
                    print(flghfrom)
                except Exception as e:
                    flghfrom = ''
                try:
                    if "Flight To :" in row:flght_to = row.split("Flight To : ") [-1] 
                    print(flght_to)
                except Exception as e:
                    flght_to = ''
                try:
                    if "GSTN :" in row: sup_gst = row.split(":")[1]
                    print(sup_gst)
                except Exception as e:
                    sup_gst =''
                try:
                    if "GSTIN of Customer" in row: cus_gst = row.split(" ")[4]
                    print(cus_gst)
                except Exception as e:
                    cus_gst = ''

            try:
                bounding_box1 = (100, 220, 240, 260)
                crop_area1 = extracted_text.crop(bounding_box1)
                crop_text1 = crop_area1.extract_text().split('\n')
                cus_name = ' '.join(crop_text1).split(':')[-1]
                print(cus_name)
            except Exception as e:
                cus_name =''

            
            core_data = table[4:8]
            columns = ["desc","sac","tax_val","nontax_val","tot_val","igst_rt","igst_amt","tot_inval"]
            dictionary = [dictionarymaker(row) for row in core_data]
            try:
                if "AirAsia (India) Private" in i : supp_name = i
                print(supp_name)
            except Exception as e:
                supp_name = ''
            
            try:
                sac = int(dictionary[0]['sac'])
                print(sac)
            except Exception:
                sac= ''
            try:
                tax_val = dictionary[3]['tax_val']
                print(tax_val)
            except Exception:
                tax_val = ''
            try:
                nontax_val = dictionary[3]['nontax_val']
                print(nontax_val)
            except Exception:
                nontax_val = ''
            try:
                tot = dictionary[3]['tot_val']
                print(tot)
            except Exception:
                tot =''
            try:
                igst_amt = dictionary[3]['igst_amt']
                print(igst_amt)
            except Exception:
                igst_amt =''
            try:
                tot_inval = dictionary[3]['tot_inval']
                print(tot_inval)
            except Exception:
                tot_inval =''
            break      


        if 'SpiceJet' in i:
            print('SpiceJet')

            supp_name = 'SpiceJet Limited'

            data = table[2:3]
            core_data = [[],[]]
            for i in data: 
                for j in i:
                    l1,l2 = split1(j)
                    core_data[0].append(l1)
                    core_data[1].append(l2)     
            for row in extracted_text.split("\n"):
                try:
                    if row.startswith("Passenger: "): pgnr_nm = row.split("Passenger: ")[-1]   
                    print(pgnr_nm)
                except Exception as e:
                    pgnr_nm = ''           
                try:
                    if row.startswith("Invoice No: "): inv_no = row.split("Invoice No: ")[-1]
                    print(inv_no)
                except Exception as e:
                    inv_no =''
                try:
                    if row.startswith("Invoice Date: "): inv_dte = row.split("Invoice Date: ")[-1].split()[0]
                    print(inv_dte)
                except Exception as e:
                    inv_dte = ''
                try:
                    if "Total Invoice Value inclusive of Taxes (in figures)" in row : tot_inval = row.split("Total Invoice Value inclusive of Taxes (in figures)")[-1]
                    print(tot_inval)
                except Exception as e:
                    tot_inval =''
                
                try:
                    if "Sector:" in row: 
                        flghfrom = row.split("Sector:")[1].split(" ")[1] 
                        flght_to = row.split("Sector:")[1].split(" ")[3]
                    print(flght_to,flghfrom)
                except Exception as e:
                    flghfrom =''
                    flght_to =''
                try:
                    if ' Customer Name:' in row: cus_name = row.split("Name:")[1].split('State')[0]
                    print(cus_name)
                except Exception as e:
                    cus_name =''
            columns = ["srno","desc_ser","sac","tax_val","nontax_val","tot_val","igst_rt","igst_amt","cgst_rt","cgst_amt","sgst_rt","sgst_amt"]
            dictionary = [dictionarymaker(row) for row in core_data]
            print(dictionary)
            try:
                sac = dictionary[0]['sac']
                tax_val = float(dictionary[0]['tax_val']) + float(dictionary[1]['tax_val'])
                nontax_val = dictionary[1]['nontax_val']
                igst_amt = dictionary[0]['igst_amt']
                cgst_amt = dictionary[0]['cgst_amt']
                sgst_amt = dictionary[0]['sgst_amt']
                print(sac,tax_val,nontax_val,igst_amt,cgst_amt,sgst_amt)
            except Exception as e:
                sac,tax_val,nontax_val,igst_amt,cgst_amt,sgst_amt = '','','','','',''
            break
        
        if 'AIR INDIA' in i:
            print('air india');
            supp_name ="AIR INDIA LTD"
    
            firstpage = pg
            #charst = firstpage.extract_words()
            charst = firstpage.extract_words()
            im = firstpage.to_image(resolution=150)
            im.draw_rects(firstpage.extract_words())
            invc3 = firstpage.extract_table()
            #print('\n')
            asd = 0
            for i in invc3:
                print(asd, invc3[asd])
                asd+=1
    
            #print(invc3)
    
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
    
            try:
                t = 0
                for w in z:
                    #print(r,'   ',z[r:r+2])
                    if " ".join(z[t:t+2]) == 'Invoice No.' or " ".join(z[t:t+2]) == 'Bill No':
                        inv_no = z[t+2]
                        break
                    t+=1
            except Exception as e:
                inv_no ='-'
    
    
            try:
                print('\n')
                x = 0
                for inv in z:
                    x+=1
                    if inv == 'Date':
                        bbb = z[x]
                        inv_dte = bbb
                        break
            except Exception as e:
                inv_dte ='-'
    
            try:
                a = 0
                for inv in z:
                    a+=1
                    if inv == 'Name':   
                        ddd = z[a:]
                        #print('List for name is:', ddd)
                        #break
                        name1 = 0
                        yyy = []
                        for aa in ddd:
                            if ddd[name1] == 'Address':
                                cc = name1
                                cus_name = " ".join(str(i) for i in ddd[:cc])  
                            name1+=1
                        break
            except Exception as e:
                cus_name ='-'
    
            try:
                thirdpage = pdf.pages[2]
                table = thirdpage.extract_table()
                
                pgnr_nm = table[2][1]
            except Exception as e:
                pgnr_nm ='-'
            
            try:
                flghfrom = table[2][3].split('-')[0]
                flght_to = table[2][3].split('-')[1]
            except Exception as e:
                flghfrom = '-'
                flght_to ='-'
    
            
            print('\n')
            try:
                b = 0
                for inv in z:
                    b+=1
                    if inv == 'GSTIN':
                        eee = z[b]
                        break
            except Exception as e:
                ee= '-'
    
            try:
                if '2.50' in invc3[2]:
                    d = 0
                    for inv in invc3[2]:
                        d+=1
                        if inv == '2.50':
                            ggg = invc3[2][d]
                            cgst_amt = ggg
                            sgst_amt = ggg
                            igst = '-'
                            break
                elif '5.00' in invc3[2]:
                    d = 0
                    for inv in invc3[2]:
                        d+=1
                        if inv == '5.00':
                            ggg = invc3[2][d]
                            igst_amt = ggg
                            cgst_amt = '-'
                            sgst_amt = '-'
                            break
            except Exception as e:
                igst_amt,cgst_amt,sgst_amt ='-','-','-'
            print('\n')
    
            try:
                tax_val = invc3[3][9]
            except Exception as e:
                tax_val ='-'
            
            try:
                nontax_val = invc3[3][6]
            except Exception as e:
                nontax_val ='-'
    
            print('\n')
            try:
                tot_inval = invc3[4][7]
            except Exception as e:
                tot_inval = '-'
            print('\n')
            try:
                sac = invc3[2][2]
            except Exception as e:
                sac ='-'

            break
        

        if 'InterGlobe Aviation' in i:

            supp_name = 'InterGlobe Aviation Limited'
            for row in extracted_text.split("\n"):
                try:
                    if "Number : " in row : inv_no = row.split("Number : ")[-1]
                    print(inv_no)
                except Exception as e:
                    inv_no =''
                try:
                    if "Date : " in row : inv_dte = row.split("Date : ")[-1]
                    print(inv_dte)
                except Exception as e:
                    inv_dte = ''
                try:
                    if "From : " in row: flghfrom = row.split("From : ")[1].split()[0]
                    print(flghfrom)
                except Exception as e:
                    flghfrom = ''
                try:
                    if "To : " in row: flght_to = row.split("To : ")[-1].split()[0]
                    print(flght_to)
                except Exception as e:
                    flght_to = ''
                try:
                    if "Customer Name :" in row : cus_name = row.split("Name :")[1]
                    print(cus_name)
                except Exception as E:
                    cus_name =''
            core_data = table[2:5]
            columns = ["desc","sac","tax_val","nontax_val","tot","igst_rt","igst_amt","cgst_rt","cgst_amt","sgst_rt","sgst_amt","cess_rt","cess_amt","tot_inval"]
            dictionary = [dictionarymaker(row) for row in core_data]

            try:
                sac = dictionary[0]['sac']
                tax_val = dictionary[-1]['tax_val']
                nontax_val = dictionary[-1]['nontax_val']
                igst_amt = dictionary[-1]['igst_rt']
                cgst_amt = dictionary[-1]['cgst_rt']
                sgst_amt = dictionary[-1]['sgst_rt']
                tot_inval = dictionary[-1]['tot_inval']
                print(sac,tax_val,nontax_val,igst_amt,cgst_amt,sgst_amt,tot_inval)
            except Exception as e:
                sac,tax_val,nontax_val,igst_amt,cgst_amt,sgst_amt,tot_inval = '','','','','','',''

        if 'MALAYSIA AIRLINES BERHAD' in i:
            print('MALAYSIA AIRLINES')

            supp_name = 'MALAYSIA AIRLINE'
            for row in extracted_text.split("\n"):
                try:
                    if "Invoice No :" in row: inv_no = row.split("Invoice No :")[-1]
                    print(inv_no)
                except Exception as e:
                    inv_no =''
                try:
                    if "Invoice Date :" in row: inv_dte = row.split("Invoice Date :")[-1].split()[0]
                    print(inv_dte)
                except Exception as e:
                    inv_dte = ''
                try:
                    if "Name" in row: cus_name = row.split(':')[-1]
                    print(cus_name)
                except Exception as e:
                    cus_name =''
            core_data = table[2:4]
            columns = ["desc","sac","tick_num","doctype","tckdte","classtyp","tax_val","nontax_val","cgst_rt","cgst_amt","sgst_rt","sgst_amt","igst_rt","igst_amt","cess_rt","cess_amt","tot_inval"]
            dictionary = [dictionarymaker(row) for row in core_data]

            try:
                sac = dictionary[0]["sac"]
                tax_val = float(dictionary[1]['tax_val'])
                nontax_val = float(dictionary[1]['nontax_val'])
                cgst_amt = float(dictionary[1]['cgst_rt'])
                sgst_amt = float(dictionary[1]['sgst_rt'])
                tot_inval = float(dictionary[1]['tot_inval'])
                sup_gst = gstin_number[1]
                cus_gst = gstin_number[0]
                print(sac,tax_val,nontax_val,igst_amt,cgst_amt,sgst_amt,tot_inval,sup_gst,cus_gst)
            except Exception as e:
                sac,tax_val,nontax_val,igst_amt,cgst_amt,sgst_amt,tot_inval,sup_gst,cus_gst = '','','','','','','','',''
            print("----------------------------->")
            break
        if 'TATA SIA Airlines' in i:

            supp_name = 'TATA SIA Airlines Limited'
            core_data = extracted_text.split("\n")
            for row in core_data:
                try:
                    if 'Name' in row and 'Invoice Date' in row : cus_name = row.split('Invoice')[0].split("Name")[1]
                    print(cus_name)
                except Exception:
                    cus_name = ''
                try:
                    if 'Airport tax amount' in row: nontax_val = float(row.split()[-1].replace(",",""))
                    print(nontax_val)
                except Exception:
                    nontax_val =''
                try:
                    if 'IGST Amount' in row: igst_amt = float(row.split()[-1].replace(",",""))
                    print(igst_amt)
                except Exception:
                    igst_amt =''
                try:
                    if 'CGST Amount' in row: cgst_amt = float(row.split()[-1].replace(",",""))
                    print(cgst_amt)
                except Exception:
                    cgst_amt =''
                try:
                    if 'SGST Amount' in row: sgst_amt = float(row.split()[-1].replace(",",""))
                    print(sgst_amt)
                except Exception:
                    sgst_amt =''
                try:
                    if 'Total taxable value' in row: tax_val = float(row.split()[-1].replace(",","")) 
                    print(tax_val)
                except Exception:
                    tax_val =''
                try:
                    if 'Passenger Name ' in row: pgnr_nm = row.split("Passenger Name ")[-1]
                    print(pgnr_nm)
                except Exception:
                    pgnr_nm =''
                try:
                    if 'SAC Code ' in row: sac = row.split("SAC Code ")[-1]
                    print(sac)
                except Exception:
                    sac =''
                try:
                    if 'Invoice No. ' in row: inv_no = row.split('Invoice No. ')[-1]
                    print(inv_no)
                except Exception:
                    inv_no =''
                try:
                    if 'Invoice Date ' in row: inv_dte = row.split('Invoice Date ')[-1]
                    print(inv_dte)
                except Exception:
                    inv_dte =''
                try:
                    if 'Total Journey ' in row: flghfrom = row.split()[-1].split('-')[0]; flght_to=row.split()[-1].split('-')[-1]
                    print(flghfrom)
                except Exception:
                    flghfrom =''
                try:
                    if '(in figures)' in row: tot_inval = float(row.split()[-1].replace(",",""))
                    print(tot_inval)
                except Exception:
                    tot_inval =''
    print("\n\nSupplier Name: ",supp_name)
    print("\n\nSupplier GST : ",sup_gst)
    print("\n\nCustomer Name: ",cus_name)
    print("\n\nCustomer GST : ",cus_gst)
    print("\n\nPassenger name %s \n\n Invoice Number %s \n\n Invoice Date %s \n\n Flight From %s \n\n Flight To %s \n\n SAC Code %s \n\n Taxable Value %s \n\n Non taxable value %s \n\n Total non tax %s \n\n IGST Amount %s \n\n CGST Amount %s \n\n SGST Amount %s \n\n Total invoice value %s" % (pgnr_nm.upper(),inv_no,inv_dte,flghfrom,flght_to,sac,tax_val,nontax_val,tot,igst_amt,cgst_amt,sgst_amt,tot_inval))
    duplicate = duplicate_bill_check(inv_no)
    
    if duplicate == 1:
        status = 'DUPLICATE'
    if duplicate ==  0:
        status = 'PROCCESSED'
    insert_into_main_table('Airline Bill',status,path,supp_name,sup_gst,cus_name,cus_gst,pgnr_nm,inv_no,inv_dte,flghfrom,flght_to,sac,tax_val,nontax_val,tot,igst_amt,cgst_amt,sgst_amt,tot_inval)
