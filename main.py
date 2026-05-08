import os

from storage_engine.buffer_manager import BufferPool
from storage_engine.page import add_record_to_page, get_record_from_page
from storage_engine.record_layout import serialize_record, deserialize_record

def main():
    db_file = "data/students.db"
    
    if os.path.exists(db_file):
        os.remove(db_file)
    
    buffer_pool = BufferPool(capacity=3)
    
    print("Inserting 20 records...")
    
    current_page_num = 0
    
    page_bytes = buffer_pool.get_page(db_file, current_page_num)
    
    for i in range(20):
        id_val = i
        name = f"Student{i}"
        grade = 10.0 + (i % 15)
        is_active = (i % 2 == 0)
        
        record_bytes = serialize_record(id_val, name, grade, is_active)
        result = add_record_to_page(page_bytes, record_bytes)
        
        if result is None:
            buffer_pool.mark_dirty(current_page_num)
            print(f"Page {current_page_num} is full (16 records). Moving to page {current_page_num + 1}...")
            
            current_page_num += 1
            page_bytes = buffer_pool.get_page(db_file, current_page_num)
            page_bytes = add_record_to_page(page_bytes, record_bytes)
            buffer_pool.mark_dirty(current_page_num)
        else:
            page_bytes = result
            buffer_pool.mark_dirty(current_page_num)
    
    target_id = 5
    target_page_num = target_id // 16
    target_slot = target_id % 16
    
    target_page_bytes = buffer_pool.get_page(db_file, target_page_num)
    record_bytes = get_record_from_page(target_page_bytes, target_slot)
    
    if record_bytes:
        rec_id, rec_name, rec_grade, rec_active = deserialize_record(record_bytes)
        print(f"Record #5: id={rec_id}, name='{rec_name}', grade={rec_grade}, is_active={rec_active}")
    
    buffer_pool.flush_all(db_file)
    print("Done.")
    
if __name__ == "__main__":
    main()