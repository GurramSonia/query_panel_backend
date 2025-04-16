from bson import ObjectId
from datetime import datetime

def convert_objectid_and_datetime(data):
    """Recursively convert ObjectId and datetime in MongoDB results."""
    if isinstance(data, dict):
        return {key: convert_objectid_and_datetime(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_and_datetime(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime):
        return data.strftime('%Y-%m-%d %H:%M:%S')
    return data
