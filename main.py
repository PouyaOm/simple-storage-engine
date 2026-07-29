import os
from storage_engine.buffer_manager import BufferPool
from storage_engine.page import add_record_to_page, get_record_from_page
from storage_engine.record_layout import serialize_record, deserialize_record
from storage_engine.course_page import add_record_to_page as add_course_to_page, get_record_from_page as get_course_from_page
from storage_engine.course_layout import serialize_course, deserialize_course
from storage_engine.index_page import init_index_page, add_index_entry, find_entry_by_id, get_all_entries
from storage_engine.file_manager import reset_read_count, get_read_count

def insert_into_index(buffer_pool_index, index_file, student_id, page_id, slot):
    current_page_num = 0
    while True:
        page_bytes = buffer_pool_index.get_page(index_file, current_page_num)
        result = add_index_entry(page_bytes, student_id, page_id, slot)
        if result is not None:
            buffer_pool_index.mark_dirty(current_page_num)
            return
        else:
            current_page_num += 1

def search_student_by_id(student_id, buffer_pool_students, students_file, buffer_pool_index, index_file):
    index_page_num = 0
    while True:
        page_bytes = buffer_pool_index.get_page(index_file, index_page_num)
        count = int.from_bytes(page_bytes[0:4], 'little')
        if count == 0 and index_page_num > 0:
            break
        result = find_entry_by_id(page_bytes, student_id)
        if result:
            page_id, slot = result
            student_page = buffer_pool_students.get_page(students_file, page_id)
            record_bytes = get_record_from_page(student_page, slot)
            if record_bytes:
                return deserialize_record(record_bytes)
            else:
                return None
        index_page_num += 1
    return None


def search_with_index(student_id, students_file, index_file):
    reset_read_count()
    buffer_pool_students = BufferPool(capacity=3)
    buffer_pool_index = BufferPool(capacity=3)

    index_page_num = 0
    found = False
    page_id = slot = None
    while True:
        idx_page = buffer_pool_index.get_page(index_file, index_page_num)
        count = int.from_bytes(idx_page[0:4], 'little')
        if count == 0 and index_page_num > 0:
            break
        res = find_entry_by_id(idx_page, student_id)
        if res:
            page_id, slot = res
            found = True
            break
        index_page_num += 1

    if not found:
        return None, get_read_count()

    data_page = buffer_pool_students.get_page(students_file, page_id)
    record_bytes = get_record_from_page(data_page, slot)
    if record_bytes:
        record = deserialize_record(record_bytes)
        return record, get_read_count()
    return None, get_read_count()

def search_without_index(student_id, students_file):
    reset_read_count()
    buffer_pool = BufferPool(capacity=3)

    page_num = 0
    while True:
        page_bytes = buffer_pool.get_page(students_file, page_num)
        record_count = int.from_bytes(page_bytes[0:4], 'little')
        if record_count == 0 and page_num > 0:
            break   
        for slot in range(record_count):
            rec_bytes = get_record_from_page(page_bytes, slot)
            if rec_bytes:
                sid, name, grade, active = deserialize_record(rec_bytes)
                if sid == student_id:
                    return (sid, name, grade, active), get_read_count()
        page_num += 1
    return None, get_read_count()

def main():
    students_file = "data/students.db"
    courses_file = "data/courses.db"
    index_file = "data/index.db"
    
    for f in [students_file, courses_file, index_file]:
        if os.path.exists(f):
            os.remove(f)
    
    buffer_pool_students = BufferPool(capacity=3)
    buffer_pool_courses = BufferPool(capacity=3)
    buffer_pool_index = BufferPool(capacity=3)
    
    print("Inserting 50 records into students and updating index...")
    current_page_num = 0
    page_bytes = buffer_pool_students.get_page(students_file, current_page_num)
    
    for i in range(150):
        id_val = i
        name = f"Student{i}"
        grade = 10.0 + (i % 15)
        is_active = (i % 2 == 0)
        record_bytes = serialize_record(id_val, name, grade, is_active)
        result = add_record_to_page(page_bytes, record_bytes)
        
        if result is None:
            buffer_pool_students.mark_dirty(current_page_num)
            current_page_num += 1
            page_bytes = buffer_pool_students.get_page(students_file, current_page_num)
            page_bytes = add_record_to_page(page_bytes, record_bytes)
            buffer_pool_students.mark_dirty(current_page_num)
            slot = 0
            page_id_for_index = current_page_num
        else:
            page_bytes = result
            buffer_pool_students.mark_dirty(current_page_num)
            count = int.from_bytes(page_bytes[0:4], 'little')
            slot = count - 1
            page_id_for_index = current_page_num
        
        insert_into_index(buffer_pool_index, index_file, id_val, page_id_for_index, slot)
    
    print("\nInserting 20 records into courses...")
    current_page_num = 0
    page_bytes = buffer_pool_courses.get_page(courses_file, current_page_num)
    for i in range(1, 21):
        course_id = i
        title = f"Course_{i}"
        credits = (i % 3) + 1
        record_bytes = serialize_course(course_id, title, credits)
        result = add_course_to_page(page_bytes, record_bytes)
        if result is None:
            buffer_pool_courses.mark_dirty(current_page_num)
            print(f"Page {current_page_num} full. Moving to next...")
            current_page_num += 1
            page_bytes = buffer_pool_courses.get_page(courses_file, current_page_num)
            page_bytes = add_course_to_page(page_bytes, record_bytes)
            buffer_pool_courses.mark_dirty(current_page_num)
        else:
            page_bytes = result
            buffer_pool_courses.mark_dirty(current_page_num)
    
    buffer_pool_students.flush_all(students_file)
    buffer_pool_courses.flush_all(courses_file)
    buffer_pool_index.flush_all(index_file)
    
    print("\n" + "="*50)
    print("Comparing search methods for student_id=130")
    print("="*50)
    
    student, io_index = search_with_index(130, students_file, index_file)
    if student:
        print(f"Index search: found {student}, I/O reads = {io_index}")
    else:
        print(f"Index search: not found, I/O reads = {io_index}")
    
    student2, io_full = search_without_index(130, students_file)
    if student2:
        print(f"Full scan search: found {student2}, I/O reads = {io_full}")
    else:
        print(f"Full scan search: not found, I/O reads = {io_full}")
    
    print("\nAll done.")

if __name__ == "__main__":
    main()