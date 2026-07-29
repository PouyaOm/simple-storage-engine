def init_index_page():
    page = bytearray(512)
    return page

def add_index_entry(page_bytes, student_id, page_id, slot):
    current_count = int.from_bytes(page_bytes[0:4], 'little')
    
    if current_count >= 42:
        return None
    
    offset = 4 + (current_count * 12)
    page_bytes[offset:offset+4] = student_id.to_bytes(4, 'little')
    page_bytes[offset+4:offset+8] = page_id.to_bytes(4, 'little')
    page_bytes[offset+8:offset+12] = slot.to_bytes(4, 'little')
    
    page_bytes[0:4] = (current_count + 1).to_bytes(4, 'little')
    return page_bytes

def get_all_entries(page_bytes):
    count = int.from_bytes(page_bytes[0:4], 'little')
    entries = []
    for i in range(count):
        offset = 4 + (i * 12)
        sid = int.from_bytes(page_bytes[offset:offset+4], 'little')
        pid = int.from_bytes(page_bytes[offset+4:offset+8], 'little')
        sl = int.from_bytes(page_bytes[offset+8:offset+12], 'little')
        entries.append((sid, pid, sl))
    return entries

def find_entry_by_id(page_bytes, target_student_id):
    count = int.from_bytes(page_bytes[0:4], 'little')
    for i in range(count):
        offset = 4 + (i * 12)
        sid = int.from_bytes(page_bytes[offset:offset+4], 'little')
        if sid == target_student_id:
            pid = int.from_bytes(page_bytes[offset+4:offset+8], 'little')
            sl = int.from_bytes(page_bytes[offset+8:offset+12], 'little')
            return (pid, sl)
    return None