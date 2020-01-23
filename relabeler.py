#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:18:58 2020

@author: kyle
"""
#%% Imports
import os
import sys
from re import sub
from argparse import ArgumentParser
from PyPDF2 import PdfFileReader
#%% Functions
def substitute_illegal_characters(text):
    return sub(r'[\(\):,/;*\]\[|\\\.]', r"_", text)

def get_new_filename(fn, directory, add_author):
    with open(os.path.join(directory, fn), "rb") as f:
        reader = PdfFileReader(f, strict=False)
        # Get Title & Author
        info = reader.getDocumentInfo()
        title = info.title
        author = info.author
        title = substitute_illegal_characters(title)
        if author and title and add_author:
            author = substitute_illegal_characters(author)
            new_fn = title + "-" + author + ".pdf"
        elif title:
            new_fn = title + ".pdf"
        else:
            print(f"Title Not Found For: {fn}")
            new_fn = fn
        return new_fn

def get_filenames(directory):
    if os.path.exists(directory):
        files = os.listdir(directory)
        files = [fn for fn in files if fn[-4:] == ".pdf"]
        return files
    else:
        raise Exception(f"The directory, '{directory}', does not exist")

def rename_file(directory, original_fn, new_fn):
    if os.path.exists(os.path.join(directory, original_fn)):
        old_path = os.path.join(directory, original_fn)
        new_path = os.path.join(directory, new_fn)
        os.rename(old_path, new_path)

def main():
    parser = ArgumentParser(description="Rename Some PDFs")
    parser.add_argument("--directory", type=str,
                        help="The directory to look for PDFs",
                        default=os.path.join(os.getcwd(),"pdfs_to_rename"))
    parser.add_argument("--author",
                        type=bool, default=False,
                        help="Add Author To New Filename [True or False]")
    args = parser.parse_args()
    directory = args.directory
    add_author = args.author
    files_to_rename = get_filenames(directory)
    try:
        for fn in files_to_rename:
            new_fn = get_new_filename(fn, directory, add_author)
            rename_file(directory, fn, new_fn)
    except:
        error = sys.exc_info()
        print("An Error(s) Has Occured!!!!")
        print(error)
    finally:
        sys.exit()

#%% Run Main
if __name__ == "__main__":
    main()