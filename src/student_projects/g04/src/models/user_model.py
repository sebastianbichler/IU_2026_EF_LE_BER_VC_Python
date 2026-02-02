class User:
    def __init__(self, name, _id=None):
        self.id = _id
        self.name = name

    @classmethod
    def from_dict(cls, data):
        # Converts MongoDB dictionary to User object
        return cls(
            name=data.get('name'),
            _id=data.get('_id')
        )

    def to_dict(self):
        # Converts User object to dictionary for MongoDB
        return {
            'name': self.name,
        }
