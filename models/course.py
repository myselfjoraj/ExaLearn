from flask_login import current_user


class Course:

    def __init__(self, id, title, description, category, price, duration, thumbnail, section, author, time):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.price = price
        self.duration = duration
        self.thumbnail = thumbnail
        self.author = author
        self.time = time
        self.section = section

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'duration': self.duration,
            'thumbnail': self.thumbnail,
            'author': self.author,
            'time': self.time,
            'section': self.section
        }

    @classmethod
    def from_dict(cls, dict_data):
        return cls(
            dict_data['id'],
            dict_data['title'],
            dict_data['description'],
            dict_data['category'],
            dict_data['price'],
            dict_data['duration'],
            dict_data['thumbnail'],
            dict_data['section'],
            dict_data['author'],
            dict_data['time']
        )
