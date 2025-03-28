import os
import sys
import glob
from PIL import Image
from pyzbar.pyzbar import decode

def list_images(folder):
    for ext in extensions:
        files.extend(glob.glob(os.path.join(folder, ext)))
    return sorted(files)

def decode_qr_image(image_path):
    img = Image.open(image_path)
    decoded_objects = decode(img)
    if not decoded_objects:
        print(f"No QR code found in {image_path}")
        return None
    return decoded_objects[0].data.decode('utf-8')

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 recombine.py [input_folder] [output_file]")
        sys.exit(1)
    
    folder = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.isdir(folder):
        print("Provided folder path is invalid.")
        sys.exit(1)
    
    image_files = list_images(folder)
    if not image_files:
        print("No image files found in the folder.")
        sys.exit(1)
    
    full_text = ""
    for image_path in image_files:
        chunk_text = decode_qr_image(image_path)
        if chunk_text is None:
            continue
        full_text += chunk_text
        print(f"Decoded chunk from {image_path} (length: {len(chunk_text)} characters)")

    header = full_text[:8]
    try:
        original_size = int(header, 16)
    except Exception as e:
        print("Error reading file size from header:", e)
        sys.exit(1)
    
    hex_data = full_text[8:]
    file_data = bytes.fromhex(hex_data)
    file_data = file_data[:original_size]
    
    with open(output_file, "wb") as f:
        f.write(file_data)
    print(f"[!] Finished!")

if __name__ == "__main__":
    main()
