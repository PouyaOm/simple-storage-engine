from .file_manager import read_page, write_page

class BufferPool:
    def __init__(self, capacity=3):
        self.capacity = capacity 
        self.pages = {} 
        self.lru = [] 
        self.dirty = set() 
        
    def  get_page(self, file, page_num):
        if page_num in self.pages:
            self.lru.remove(page_num)
            self.lru.append(page_num)
            return self.pages[page_num]
        
        page_bytes = read_page(file, page_num)
        if len(self.pages) >= self.capacity:
            oldest = self.lru.pop(0)
            
            if oldest in self.dirty:
                write_page(file, oldest, self.pages[oldest])
                print(f"Flushed page {oldest} to disk")
                self.dirty.remove(oldest)
            
            del self.pages[oldest]
            print(f"Buffer evicted: page {oldest}")
        
        self.pages[page_num] = page_bytes
        self.lru.append(page_num)
        return page_bytes


    def mark_dirty(self, page_num):
        if page_num in self.pages:
            self.dirty.add(page_num)
        
        
    def flush_all(self, file):
        for page_num in list(self.dirty):
            write_page(file, page_num, self.pages[page_num])
            print(f"Flushed page {page_num} to disk")
        self.dirty.clear()