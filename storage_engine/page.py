def init_page():
    page = bytearray(512)
    page[0:4] = (0).to_bytes(4, byteorder="little")
    return page


def add_record_to_page(page_bytes, record_bytes):
    current_count = int.from_bytes(page_bytes[0:4], byteorder="little") 
    
    if current_count >= 16:
        return None
    
    slot_offset = 4 + (current_count * 30)
    
    page_bytes[slot_offset:slot_offset + 30] = record_bytes
    
    page_bytes[0:4] = (current_count + 1).to_bytes(4, byteorder="little")

    return page_bytes


def get_record_from_page(page_bytes, slot):
    if slot < 0 or slot >= 16:
        return None
    
    record_count = int.from_bytes(page_bytes[0:4], byteorder="little")
    if slot >= record_count:
        return None
    
    slot_offset = 4 + (slot * 30)
    return bytes(page_bytes[slot_offset:slot_offset + 30])