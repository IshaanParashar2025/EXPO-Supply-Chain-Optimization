"""JSON serialization helpers for MongoDB documents."""
from bson import ObjectId


def serialize_doc(doc):
    """Recursively convert ObjectId instances to strings in a document."""
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}
    if isinstance(doc, ObjectId):
        return str(doc)
    return doc

