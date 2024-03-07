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
config_obj.read('/home/shashi/Documents/WorkingFolder/venv/afcons/tele_render/config.ini')

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
def duplicate_bill_check(bill_no):
    list_connection('TelePhoneBills')
    paged_items = tasks_list.items.get().execute_query()
    for index, item in enumerate(paged_items): 
        if bill_no == item.properties.get("bill_no"):
            print(item.properties.get('RequestNo'))
            return 1
    return 0

def insert_into_main_table(bill_name,status,employee_name,bill_no,bill_period_from,bill_period_to,bill_date,telephone_no,bill_amount,cgst,sgst,total_amount,path,taxes,taxable,non_taxable,ship_to_state_code,supply): 
    list_connection('TelePhoneBills')
    try:
        items = tasks_list.items.get().execute_query()
        idlist =[]
        for item in items: 
            idlist.append(item.properties.get("RequestNo"))
        last_req = idlist[-1]
        last_req = last_req.split('-')
        last_req = literal_eval(last_req[1])
        new_req = f'REQ-{last_req+1}'

    except Exception as te:
        new_req = 'REQ-1'
    bill_period_from =try_parsing_date(bill_period_from)
    bill_period_to = try_parsing_date(bill_period_to)
    bill_date = try_parsing_date(bill_date)
    try:
        task_item = tasks_list.add_item(
            {
                'RequestNo' : str(new_req),
                'status' : str(status),
                'bill_name' : str(bill_name),
                'emp_name' : str(employee_name),
                'bill_no' : str(bill_no),
                'bill_period_from' : str(bill_period_from),
                'bill_period_to' : str(bill_period_to),
                'bill_date' : str(bill_date),
                'telephone_no' : str(telephone_no),
                'bill_amount' : str(bill_amount),
                'cgst' : str(cgst),
                'sgst' : str(sgst),
                'taxable' : str(taxable),
                'non_taxable' :str(non_taxable),
                'ship_to_state_code' : str(ship_to_state_code),
                'supply' :str(supply),
                'taxes' : str(taxes),
                'total_amount' : str(total_amount)
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
    for fmt in ('%d­%b­%Y','%d-%b-%y','%d-%m-%Y','%d-%b-%Y','%d%b%Y','%d-%b-%Y','%d-%b-%y','%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y' , "%d %b %Y"):
        try:
            
            input_date = datetime.strptime(text, fmt)
            output_format = "%d/%m/%Y"

            # Convert the datetime object to a string with the desired output format
            output_date_string = input_date.strftime(output_format)

            return output_date_string

        except ValueError:
            pass
