from PIL import Image
from io import BytesIO
import binascii
from pathlib import Path
from multiprocessing import Pool
import os
import sys
import json

from sentry_sdk import capture_exception
import fitz
import pytesseract
from tqdm import tqdm
from tabulate import tabulate

from backend.constants import DocumentHandler 

extraction_path = DocumentHandler.extract_folder
encode_text = lambda a: binascii.hexlify(a.encode("utf8")).decode("ascii")

def extract_files(doc_paths):
    p = Pool(len(doc_paths))
    p.map(extract_and_save, doc_paths)

def extract(doc_path, stateful=True):
    pytesseract.pytesseract.tesseract_cmd = DocumentHandler.tesseract_binary
    doc = fitz.open(doc_path) # open a documents
    
    doc_name = Path(doc_path).stem
    if stateful:
        data_save_path = Path(extraction_path, doc_name)
        if os.path.exists(data_save_path):
            os.rmdir(data_save_path)
        
        os.mkdir(data_save_path)

    doc_data = []
    for page_index, page in enumerate(doc): # iterate over pdf pages
        img_list = page.get_images()
        tabs_list = page.find_tables()  # detect the tables

        # print the number of imgs found on the page
        mesg = f"{doc_name} Found "
        mesg += f"{len(img_list)} imgs, "
        mesg += f"{len(tabs_list.tables)} tables, "
        print(mesg) # TODO: SETUP PROPPER LOGGING
        #pbar.set_description(f"{mesg} On page {page_index}")

        text = page.get_text()
        data_tabs = []
        data_imgs = []
        
        for img_index, img in enumerate(img_list, start=1): # enumerate the img list
            xref = img[0] # get the XREF of the img
            pix = fitz.Pixmap(doc, xref) # create a Pixmap

            if pix.n - pix.alpha > 3: # CMYK: convert to RGB first
                pix = fitz.Pixmap(fitz.csRGB, pix)

            img_bytes = Image.open(BytesIO(pix.pil_tobytes(format="png")))
            
            img_text = pytesseract.image_to_string(img_bytes)
            img_name = f"img_{page_index}.{img_index}.png"
            
            if stateful:
                pix.save(Path(data_save_path, img_name))
            img_data = {
                "extracted_text": (img_text),
                "img_name": img_name
            }
            data_imgs.append(img_data)
        
        for tabs_index, tabs in enumerate(tabs_list.tables):
            tabs_df = tabs.to_pandas()
            tabs_tabulated = tabulate(tabs_df)
            
            tabs_data = {
                "extracted_text": (tabs_tabulated),
                "tab_name": f"tab_{tabs_index}"
            }
            data_tabs.append(tabs_data)
        
        extarcted_text = ""
        
        for idx, image in enumerate(data_imgs):
            extarcted_text += image["img_name"]  + "\n"
            extarcted_text += image["extracted_text"]  + "\n"

            data_imgs[idx] = {
                "img_name": image["img_name"],
                "extracted_text": encode_text(image["extracted_text"])
            }
        
        for idx, tabs in enumerate(data_tabs):
            extarcted_text += tabs["tab_name"] + "\n"
            extarcted_text += tabs["extracted_text"]  + "\n"

            data_tabs[idx] = {
                "img_name": tabs["tab_name"],
                "extracted_text": tabs(image["extracted_text"])
            }
        
        page_data = {
            "page_idx":page_index,
            "page_text": (text),
            "page_tables": data_tabs,
            "page_images": data_imgs,
            "full_text": extarcted_text
        }
        doc_data.append(page_data)
    return {
            "doc_name": doc_name,
            "pages_data": doc_data
        }, doc_name

def extract_and_save(filename):
    try:
        extracted_pdf, doc_name = extract(Path(DocumentHandler.upload_folder, filename))
        with open(Path(extraction_path, doc_name, "record.json"), "w") as f: 
            json.dump(extracted_pdf, f) # TODO: Add doc_date to document metadata record
    except Exception as e:
        capture_exception(e)