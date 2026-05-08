from storage_engine.record_layout import serialize_record , deserialize_record

data = serialize_record(1, "Ali", 18.5, True)
print(data)
print(len(data))
print(deserialize_record(data))

