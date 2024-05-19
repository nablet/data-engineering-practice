import zipfile
import os

def extract_csv_from_zip(file: str, dest: str):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(dest)
    os.remove(file)
