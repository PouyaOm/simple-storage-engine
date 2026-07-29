def init_page():
    page = bytearray(512)
    return page

def add_record_to_page(page_bytes, record_bytes):
    current_count = int.from_bytes(page_bytes[0:4], 'little')
    
    if current_count >= 18:         
        return None
    
    slot_offset = 4 + (current_count * 28)   
    page_bytes[slot_offset:slot_offset + 28] = record_bytes
    
    page_bytes[0:4] = (current_count + 1).to_bytes(4, 'little')
    
    return page_bytes

def get_record_from_page(page_bytes, slot):
    record_count = int.from_bytes(page_bytes[0:4], 'little')
    if slot >= record_count:
        return None
    
    slot_offset = 4 + (slot * 28)
    return page_bytes[slot_offset:slot_offset + 28]