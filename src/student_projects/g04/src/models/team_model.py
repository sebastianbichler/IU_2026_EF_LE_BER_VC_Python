from .entity_model import Entity

class Team(Entity):
    def __init__(self, name, logo_url, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.logo_url = logo_url

    @classmethod
    def from_dict(cls, data):
        # Converts MongoDB dictionary to Team object
        return cls(
            name=data.get('name'),
            logo_url=data.get('logo_url'),
            id=str(data.get('_id')),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self, for_db=False):
        # Converts Team object to dictionary (for MongoDB if for_db=True)
        data = {
            'name': self.name,
            'logo_url': self.logo_url,
        }

        super_data = super().to_dict(for_db=for_db)
        data.update(super_data)

        return data
