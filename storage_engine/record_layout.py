import struct

def serialize_record(id, name, grade, is_active):

    
    id_in_bytes = id.to_bytes(4,'little')
    
    name_in_bytes = name.encode("utf-8")[:20]
    name_in_bytes = name_in_bytes.ljust(20, b' ')

    grade_in_bytes = struct.pack('<f', grade)
    
    is_active_in_bytes = int(is_active).to_bytes(1, "little")
    
    null_bitmap = (0).to_bytes(1, "little")

    record = id_in_bytes + name_in_bytes + grade_in_bytes + is_active_in_bytes + null_bitmap   
    
    return record


def deserialize_record(data):
    id = int.from_bytes(data[0:4],'little')
    raw_name = data[4:24]
    name = data[4:24].decode('utf-8').strip()
    grade = struct.unpack('<f', data[24:28])[0]
    is_active = (data[28] == 1)
    
    return id, name, grade, is_active

