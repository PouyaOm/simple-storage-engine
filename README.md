# Simple Storage Engine

A simple database storage engine implemented for the **Database Implementation** course (Spring 2026).

## Covered Topics

- Record Layout
- Page Layout
- File Manager
- Buffer Manager (LRU)

## Page Format

- Page size: **512 bytes**
- Header size: **4 bytes**
- Record size: **30 bytes**

## Project Structure

storage_engine/
    record.py
    page.py
    file_manager.py
    buffer_manager.py



## Description

This project implements a simplified storage engine similar to those used in database systems.  
It includes record serialization, fixed-size pages, disk page management, and an in-memory buffer pool using the **LRU replacement policy**.
