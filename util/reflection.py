def populate_object(obj, data: dict):
    for key, value in data.items():
        if hasattr(obj, key) and value is not None:
            setattr(obj, key, value)
    return obj
