import os
import glob
import pdfplumber
from pathlib import Path
from urllib.error import HTTPError
import shutil
import pathlib
import datetime
import json
import configparser
# import logging
# import logging.config
import re
import time
import sys
import time
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from office365.runtime.client_request_exception import ClientRequestException
from ast import literal_eval
from string import ascii_lowercase
from itertools import groupby
# import pandas as pd
from office365.sharepoint.files.move_operations import MoveOperations
from airtel_ext import airext
from mtnl_ext import mtnlext

config_obj = configparser.ConfigParser()
config_obj.read('/code/config.ini')

sppaths = config_obj['spdl_path']
spparam = config_obj['spdoclib']
sprlpath = config_obj['sp_relative_path']
fol_loc = config_obj['folder_path']

spsite = spparam['rootsite']
spdoclib = spparam['site_url']
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
sprproot= sprlpath['root']
sprpproblem = sprlpath['problematic']
sprpduplicate = sprlpath['duplicate'] ###Add duplicate path

def move_to_folder_processed(folder):
    file_from = ctx.web.get_folder_by_server_relative_url(folder)

    file_to = file_from.move_to(sprppro).execute_query()
    print("'{0}' moved into '{1}'".format(folder, sprppro))

def try_get_folder(url):
    try:
        return ctx.web.get_folder_by_server_relative_url(url).get().execute_query()
    except ClientRequestException as e:
        if e.response.status_code == 404:
            return None
        else:
            raise ValueError(e.response.text)
        
ctx = ClientContext(spdoclib).with_credentials(ClientCredential(cid, cs))

root_folder = ctx.web.get_folder_by_server_relative_path(sproot)
pro_folder = ctx.web.get_folder_by_server_relative_path(spprocessed)
                                                                                                                                                        
def try_get_folder(url):
    try:
        return ctx.web.get_folder_by_server_relative_url(url).get().execute_query()
    except ClientRequestException as e:
        if e.response.status_code == 404:
            return None
        else:
            raise ValueError(e.response.text)
        
root_folder.expand(["Folders"]).get().execute_query()
metaurl = ''

for folder in root_folder.folders:
    folder = try_get_folder(folder.serverRelativeUrl)
    files = folder.get_files(True).execute_query()
    print(folder)
    for f in files:
        text =''
        words =[]
        metaurl = f.properties['ServerRelativeUrl']
        finalurl = spsite+metaurl
        file_name = os.path.basename(finalurl)
        path = os.path.join(lsppath, file_name)

        with open(path,'wb') as local_file:
            p_file = ctx.web.get_file_by_server_relative_url(metaurl).download(local_file).execute_query()
    
        if '.pdf' in file_name or '.PDF' in file_name:
            print('pdf',file_name)
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:                    
                    page_words = page.extract_words()
                    words.extend([word['text'] for word in page_words])
                    text += page.extract_text()
            
            if "Bharti Airtel" in text:
                airext(path)
                # exec(open(r'D:\TELEPHONE_BILLS\airtel_bill.py').read(), {'path': path })    
            if "Mahanagar" in text:
                mtnlext(path)
                print('IT is MTNL')
                # exec(open(r'D:\TELEPHONE_BILLS\MTNL_pdfplumber.py').read(), {'path': path })
        time.sleep(5)
        os.remove(file_name)
    move_to_folder_processed(folder.serverRelativeUrl)
    print('Moved folder:', folder)




