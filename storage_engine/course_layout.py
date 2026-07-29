import struct

def serialize_course(course_id, title, credits):

    course_id_bytes = course_id.to_bytes(4, 'little')
    
    title_bytes = title.encode('utf-8')[:20]
    title_bytes = title_bytes.ljust(20, b' ')
    
    credits_bytes = credits.to_bytes(4, 'little')
    
    record = course_id_bytes + title_bytes + credits_bytes
    return record

def deserialize_course(data):
    
    course_id = int.from_bytes(data[0:4], 'little')
    title = data[4:24].decode('utf-8').strip()
    credits = int.from_bytes(data[24:28], 'little')
    return course_id, title, credits