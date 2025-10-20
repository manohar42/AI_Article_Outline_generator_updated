# src/utils/access.py
def get_attr(obj, name, default=None):
    """
    Safe accessor that supports both attribute and dict access.
    Example: get_attr(keywords, "primary") works for Pydantic model or dict.
    """
    if obj is None:
        return default
    if hasattr(obj, name):
        return getattr(obj, name, default)
    if isinstance(obj, dict):
        return obj.get(name, default)
    return default
