# coding: utf-8

import re

def get_dir_name(url: str)-> str:
    """
    generate a directory
    """
    l = url.split("/")
    dir_string =  "/".join(l[2:len(l)-1])
    return "modules/"+dir_string

def get_filename(cd)->str or None:
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

