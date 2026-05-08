from storage_engine.page import init_page, add_record_to_page, get_record_from_page
from storage_engine.record_layout import serialize_record, deserialize_record
from storage_engine.file_manager import write_page, read_page

FILE = "data/test.db"

page = init_page()

rec1 = serialize_record(1, "Ali", 18.5, True)
rec2 = serialize_record(2, "Sara", 19.0, False)

add_record_to_page(page, rec1)
add_record_to_page(page, rec2)

write_page(FILE, 0, page)

print("Page written to disk")

page_from_disk = read_page(FILE, 0)

print("Page read from disk")

count = int.from_bytes(page_from_disk[0:4], "little")
print("Record count:", count)

r1 = get_record_from_page(page_from_disk, 0)
r2 = get_record_from_page(page_from_disk, 1)

print("Record 1:", deserialize_record(r1))
print("Record 2:", deserialize_record(r2))
