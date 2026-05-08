import os

def  write_page(file, page_num, page_bytes):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if not os.path.exists(file):
        with open(file, "wb") as f:
            pass
    
    with open(file, "rb+") as f:
        f.seek(page_num * 512)
        f.write(page_bytes)
        f.flush()

        
def read_page(file, page_num):
    if not os.path.exists(file):
        return None
    
    with open(file, "rb") as f:
        f.seek(page_num * 512)
        data = f.read(512)
        
    
    if len(data) < 512:
        return None
    
    return bytearray(data)
