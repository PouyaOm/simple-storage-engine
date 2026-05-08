import struct

def serialize_record(id, name, grade, is_active):

    
    id_in_bytes = id.to_bytes(4, byteorder='little', signed='True')
    
    name_in_bytes = name.encode("utf-8")
    name_in_bytes = name_in_bytes.ljust(20, b' ')

    grade_in_bytes = struct.pack('<f', grade)
    
    is_active_in_bytes = int(is_active).to_bytes(1, "little")
    
    null_bitmap = (0).to_bytes(1, "little")

    record = id_in_bytes + name_in_bytes + grade_in_bytes + is_active_in_bytes + null_bitmap
    
    assert len(record) == 30, f"Record size is not {30} bytes"
    
    return record


def deserialize_record(data):
    
    if len(data) != 30:
        raise ValueError(f"Record must be {30} bytes")
    
    id = int.from_bytes(data[0:4], byteorder='little', signed=True)
    raw_name = data[4:24]
    name = raw_name.decode('utf-8').strip()
    grade = struct.unpack('<f', data[24:28])[0]
    is_active = (data[28] == 1)
    
    return id, name, grade, is_active

