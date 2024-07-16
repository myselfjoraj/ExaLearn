class Comments:
    def __init__(self, id, comment, time, user, is_faculty):
        self.id = id
        self.comment = comment
        self.time = time
        self.user = user
        self.is_faculty = is_faculty

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'time': self.time,
            'user': self.user,
            'is_faculty': self.is_faculty
        }

    @classmethod
    def from_dict(cls, dict_data):
        return cls(
            dict_data['id'],
            dict_data['comment'],
            dict_data['time'],
            dict_data['user'],
            dict_data['is_faculty']
        )
