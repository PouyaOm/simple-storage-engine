import os

def  write_page(file_path, page_num, page_bytes):
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            pass
    
    with open(file_path, "rb+") as f:
        f.seek(page_num * 512)
        f.write(page_bytes)

        
def read_page(file_path, page_num):
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "rb") as f:
        f.seek(page_num * 512)
        data = f.read(512)
        if len(data) < 512:
            return None
        return bytearray(data)
