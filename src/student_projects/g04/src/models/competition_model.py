from .entity_model import Entity

class Competition(Entity):
    def __init__(self, name, description, logo_url, start_date, end_date, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.description = description
        self.logo_url = logo_url
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def from_dict(cls, data):
        # Converts MongoDB dictionary to Competition object
        return cls(
            name=data.get('name'),
            description=data.get('description'),
            logo_url=data.get('logo_url'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            id=str(data.get('_id')),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self, for_db=False):
        # Converts Competition object to dictionary (for MongoDB if for_db=True)
        data = {
            'name': self.name,
            'description': self.description,
            'logo_url': self.logo_url,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }

        super_data = super().to_dict(for_db=for_db)
        data.update(super_data)

        return data
