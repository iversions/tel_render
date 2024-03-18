# from core_function import corefc
# from corefunction import corefc
#from checkdt import checkdate
from pathlib import Path
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.runtime.auth.token_response import TokenResponse
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from office365.runtime.client_request_exception import ClientRequestException
from ast import literal_eval
from string import ascii_lowercase
from itertools import groupby
import configparser

import os
from office365.sharepoint.attachments.creation_information import (
    AttachmentCreationInformation,
)



config_obj = configparser.ConfigParser()
config_obj.read('/code/config.ini')

sppaths = config_obj['spdl_path']
spparam = config_obj['spdoclib']
sprlpath = config_obj['sp_relative_path']
fol_loc = config_obj['folder_path']

spsite = spparam['rootsite']
spdoclib = spparam['site_url']
splistname = spparam['list_name']
spusername = spparam['uname']
sppassword = spparam['upass']
cid = spparam['cid']
cs = spparam['cs']

sproot = sppaths['root']
spprocessed = sppaths['processed']
spproblematic = sppaths['problematic']
spduplicate = sppaths['duplicate'] ###Add duplicate path

lsppath = fol_loc['spdl']

sprppro = sprlpath['processed']
sprpproblem = sprlpath['problematic']
sprpduplicate = sprlpath['duplicate'] ###Add duplicate path

global tasks_list
def list_connection(list_name):
    global tasks_list
    try:
        ctx = ClientContext(spdoclib).with_credentials(ClientCredential(cid, cs))
        list_title = list_name
        tasks_list = ctx.web.lists.get_by_title(list_title)

    except Exception as e:
        if e.response.status_code == 404:
            print(None)
        else:
            print(e.response.text)

def duplicate_bill_check(inv_no):
    list_connection('IProv1')
    paged_items = tasks_list.items.get().execute_query()
    for index, item in enumerate(paged_items): 
        if inv_no == item.properties.get("Invoice_no"):
            print(item.properties.get('RequestNo'))
            return 1
    return 0


def insert_into_main_table(title,status,path,supp_name,sup_gst,cus_name,cus_gst,pgnr_nm,inv_no,inv_dte,flghfrom,flght_to,sac,tax_val,nontax_val,tot,igst_amt,cgst_amt,sgst_amt,tot_inval): 
    list_connection('IProv1')
    try:
        items = tasks_list.items.get().execute_query()
        idlist =[]
        for item in items:  # type:ListItem
            idlist.append(item.properties.get("RequestNo"))
        last_req = idlist[-1]
        last_req = last_req.split('-')
        last_req = literal_eval(last_req[1])
        new_req = f'REQ-{last_req+1}'

    except Exception as te:
        new_req = 'REQ-1'
    inv_dte =try_parsing_date(inv_dte)
    try:
        task_item = tasks_list.add_item(
            {
                'Bill_Type' : str(title),
                'status' : str(status)
                'RequestNo' : str(new_req),
                'Supplier_nm'  :str(supp_name),
                'Supplier_gst' : str(sup_gst),
                'Customer_nm' : str(cus_name),
                'Customer_gst': str(cus_gst),
                'Passenger_nm'  :str(pgnr_nm),
                'Invoice_no' : str(inv_no),
                'Invoice_date'  :str(inv_dte),
                'Flight_from' : str(flghfrom),
                'Flight_To' : str(flght_to),
                'Taxable_value' :str(tax_val),
                'NonTaxable_vl'  : str(nontax_val),
                'IGST_amount'  :str(igst_amt),
                'CGST_amount' : str(cgst_amt),
                'SGST_amount' : str(sgst_amt),
                'Total_amount' : str(tot_inval)
            }
        ).execute_query()

        print('Inserted in List')
        with open(path, "rb") as fh:
            file_content = fh.read()
            attachment_file_info = AttachmentCreationInformation(
                os.path.basename(path), file_content
            )
        attachment = task_item.attachment_files.add(attachment_file_info).execute_query()
        print(attachment.server_relative_url)

    except Exception as e:
        if e.response.status_code == 404:
            print(None)
        else:
            print(e.response.text) 
      
from datetime import datetime

def try_parsing_date(text):
    for fmt in ('%d­%b­%Y','%d-%b-%y','%d-%m-%Y','%d-%b-%Y','%d%b%Y','%d-%b-%Y','%d-%b-%y','%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y','%d/%m/%y'):
        try:
            
            input_date = datetime.strptime(text, fmt)
            output_format = "%d/%m/%Y"

            # Convert the datetime object to a string with the desired output format
            output_date_string = input_date.strftime(output_format)

            return output_date_string

        except ValueError:
            pass
    
def insert_VIP(title,path,bill_address,supplier_address,PO_num,PO_date,PO_valid_date,quantity,taxable_amount,SGST,CGST,grand_total,sup_gst,cus_gst): 
    list_connection('IProv1')
    try:
        items = tasks_list.items.get().execute_query()
        idlist =[]
        for item in items:  # type:ListItem
            idlist.append(item.properties.get("RequestNo"))
        last_req = idlist[-1]
        last_req = last_req.split('-')
        last_req = literal_eval(last_req[1])
        new_req = f'REQ-{last_req+1}'

    except Exception as te:
        new_req = 'REQ-1'
    
    PO_date = try_parsing_date(PO_date)
    PO_valid_date = try_parsing_date(PO_valid_date)
    try:
        task_item = tasks_list.add_item(
            {
                'Bill_Type' : str(title),
                'RequestNo' : str(new_req),
                'V_supp_add'  :str(supplier_address),
                'V_bill_add' : str(bill_address),
                'V_PO_num' : str(PO_num),
                'V_PO_date': str(PO_date),
                'V_PO_vdate'  :str(PO_valid_date),
                'V_qnty' : str(quantity),
                'Taxable_value' :str(taxable_amount),
                'CGST_amount' : str(CGST),
                'SGST_amount' : str(SGST),
                'Supplier_gst' : str(sup_gst),
                'Customer_gst': str(cus_gst),                
                'Total_amount' : str(grand_total)
            }
        ).execute_query()

        print('Inserted in List')
        with open(path, "rb") as fh:
            file_content = fh.read()
            attachment_file_info = AttachmentCreationInformation(
                os.path.basename(path), file_content
            )
        attachment = task_item.attachment_files.add(attachment_file_info).execute_query()
        print(attachment.server_relative_url)

    except Exception as e:
        if e.response.status_code == 404:
            print(None)
        else:
            print(e.response.text) 


def Untrained(path,inv_no,inv_date,inv_total,gst1,gst1_name, gst1_addr,gst2,gst2_name, gst2_addr,line_item):
    list_connection('UnTrained_INV')
    try:
        items = tasks_list.items.get().execute_query()
        idlist =[]
        for item in items:  # type:ListItem
            idlist.append(item.properties.get("RequestNo"))
        last_req = idlist[-1]
        last_req = last_req.split('-')
        last_req = literal_eval(last_req[1])
        new_req = f'REQ-{last_req+1}'

    except Exception as te:
        new_req = 'REQ-1'
    
    inv_date = try_parsing_date(inv_date)
    if inv_date == None:
        inv_date = '-'
    try:
        task_item = tasks_list.add_item(
            {
                'RequestNo' : str(new_req),
                'Invoice_no' : str(inv_no),
                'Invoice_date' : str(inv_date),
                'Inv_total' : str(inv_total),
                'gst_1' : str(gst1),
                'gst1_name'  : str(gst1_name),
                'gst1_addr'  : str(gst1_addr),
                'gst_2' : str(gst2),
                'gst2_name'  : str(gst2_name),
                'gst2_addr'  : str(gst2_addr),
            }
        ).execute_query()

        print('Inserted in untrained')
        with open(path, "rb") as fh:
            file_content = fh.read()
            attachment_file_info = AttachmentCreationInformation(
                os.path.basename(path), file_content
            )
        attachment = task_item.attachment_files.add(attachment_file_info).execute_query()
        print(attachment.server_relative_url)

    except Exception as e:
        if e.response.status_code == 404:
            print(None)
        else:
            print('########',e.response.text) 
    
    list_connection('UnTrained_List')

    try:
        task_item = tasks_list.add_item(
            {
                'RequestNo' : str(new_req),
                'Line_Item'  : str(line_item),
            }
        ).execute_query()

        print('Inserted Line Item')
    except Exception as e:
        if e.response.status_code == 404:
            print(None)
        else:
            print(e.response.text)

