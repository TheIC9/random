import os, re, hashlib
import pandas as pd
import gdown
from supabase import create_client
from parse_resume import parse_pdf  # we'll define this later
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
print("ENV file present? ->", os.path.isfile(".env"))
print("SUPABASE_URL raw ->", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY raw ->", os.getenv("SUPABASE_KEY"))

SUPABASE_URL = os.getenv("https://mwqqwdzayneuaexoolfw.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im13cXF3ZHpheW5ldWFleG9vbGZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxMjM5MDgsImV4cCI6MjA3MzY5OTkwOH0.DaRvh7rLS9g-V6OQLzZtp7x1051A2D7kNschgfgmLyA")
DOWNLOAD_DIR = "../downloads"
BUCKET = "GITAM Hyd_2026 batch students list with CV link_Signode"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def extract_drive_id(url):
    # Handles common patterns
    patterns = [
        r"/d/([a-zA-Z0-9_-]+)",      # /d/FILEID
        r"id=([a-zA-Z0-9_-]+)",      # ?id=FILEID
        r"drive.google.com/file/d/([a-zA-Z0-9_-]+)"
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def download_public_drive(file_id, out_path):
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    return gdown.download(url, out=out_path, quiet=False)

def upload_to_supabase(local_path, storage_path):
    with open(local_path, "rb") as f:
        res = supabase.storage.from_(BUCKET).upload(storage_path, f)  # may return dict
    return res

def insert_metadata(file_name, storage_path, drive_link, file_hash, parsed, text):
    data = {
        "file_name": file_name,
        "storage_path": storage_path,
        "drive_link": drive_link,
        "file_hash": file_hash,
        "parsed_data": parsed,
        "text_content": text
    }
    supabase.table("resumes").insert(data).execute()

def main():
    df = pd.read_csv("../data/GITAM Hyd_2026 batch students list with CV link_Signode.csv")
    links = df["drive_link"].dropna().unique()

    for url in links:
        file_id = extract_drive_id(url)
        if not file_id:
            print("Could not extract ID for:", url)
            continue
        fname = f"{file_id}.pdf"
        local_path = os.path.join(DOWNLOAD_DIR, fname)

        # download
        download_public_drive(file_id, local_path)

        # dedup via hash
        file_hash = sha256(local_path)
        exists = supabase.table("resumes").select("id").eq("file_hash", file_hash).execute()
        if exists.data and len(exists.data) > 0:
            print("File already uploaded, skipping:", fname)
            os.remove(local_path)
            continue

        # parse (returns parsed dict + full text)
        parsed, text = parse_pdf(local_path)

        # upload to supabase storage
        storage_path = f"resumes/{fname}"
        upload_to_supabase(local_path, storage_path)

        # insert metadata row
        insert_metadata(fname, storage_path, url, file_hash, parsed, text)

        # cleanup local
        os.remove(local_path)
        print("Processed:", fname)

if __name__ == "__main__":
    main()
