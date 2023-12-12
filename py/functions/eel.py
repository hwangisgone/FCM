"""
Any callable in this file will be automatically exposed to eel at runtime.
Write everything you need here.
"""
import tkinter
from tkinter import filedialog as fd
import logging
import eel
import requests

from .fcm import marketing_campaign, load_data_csv, get_original_df

def choose_file() -> str:
    tkinter.Tk().withdraw()
    root = tkinter.Tk()
    root.attributes("-alpha", 0.0)
    root.attributes("-topmost", True)
    filename = fd.askopenfilename(
        parent=root, title="Choose a file", filetypes=[("All files", "*.csv")]
    )
    root.destroy()
    return filename

