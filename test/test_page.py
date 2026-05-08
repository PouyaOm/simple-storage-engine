from storage_engine.page import *
from storage_engine.record_layout import serialize_record, deserialize_record

page = init_page()

rec1 = serialize_record(1, "Ali", 18.5, True)
rec2 = serialize_record(2, "Sara", 19.0, False)

add_record_to_page(page, rec1)
add_record_to_page(page, rec2)

print(int.from_bytes(page[0:4], "little")) 

record = get_record_from_page(page, 1)
print(deserialize_record(record))  
print(len(record))
