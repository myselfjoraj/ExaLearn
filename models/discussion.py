from models.comments import Comments


class Discussion:
    def __init__(self, id, title, desc, category, ask, time, comments=None):
        self.id = id
        self.title = title
        self.desc = desc
        self.category = category
        self.ask = ask
        self.time = time
        self.comments = comments if comments is not None else []

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'category': self.category,
            'ask': self.ask,
            'time': self.time,
            'comments': [comment.to_dict() for comment in self.comments]
        }

    @classmethod
    def from_dict(cls, dict_data):
        comments_data = dict_data.get('comments', [])
        comments = [Comments.from_dict(comment_data) for comment_data in comments_data]
        return cls(
            dict_data['id'],
            dict_data['title'],
            dict_data['desc'],
            dict_data['category'],
            dict_data['ask'],
            dict_data['time'],
            comments
        )
