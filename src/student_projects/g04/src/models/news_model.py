class News:
    def __init__(self, title, content, _id=None, image=None):
       self.id = _id      
       self.title = title
       self.content = content
       self.image = image

    @classmethod
    def from_dict(cls, data):
        return cls(title = data.get('title'),
                   content = data.get('content'),
                     image=data.get('image'),
                   _id=data.get('_id'))
    
    def to_dict(self):
        return {
            'title' : self.title,
            'content' : self.content,
            'image': self.image
        }

