"""Adapter pattern example
The Adapter Pattern allows incompatible interfaces to work together. A great example in Python is custom serialization with json.dump() and json.JSONEncoder.
"""

# ❓ Problem Statement
# Python's built-in json.dump() only works with basic data types (str, int, dict, etc.). If you try to serialize a custom object directly, it fails:


import json


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


user = User("Alice", 25)

# This will raise TypeError: Object of type 'User' is not JSON serializable
print(json.dumps(user))


# We create a custom adapter by extending json.JSONEncoder to make User objects compatible with json.dump().
class UserAdapter(json.JSONEncoder):
    """
    How This is an Adapter ❓
    UserAdapter acts as a bridge between the User class and json.dump(), which originally doesn't support User.
    It adapts the User object to a JSON-compatible format (dict).
    The incompatible interface (User) becomes compatible with json.dump().
    """

    def default(self, obj):
        if isinstance(obj, User):
            return {"name": obj.name, "age": obj.age}
        return super().default(obj)  # Fallback to default encoding


# Now, we can serialize a User object using our adapter
print(json.dumps(user, cls=UserAdapter))  # o/p-> {"name": "Alice", "age": 25}
