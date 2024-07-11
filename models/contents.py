from flask import json


class Contents:

    def __init__(self, id, title, desc, duration, url=None):
        self.id = id
        self.title = title
        self.desc = desc
        self.duration = duration
        self.url = url

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'duration': self.duration,
            'url': self.url
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            title=data['title'],
            desc=data['desc'],
            duration=data['duration'],
            url=data['url']
        )


