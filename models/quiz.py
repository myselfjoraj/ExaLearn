from flask import json


class Quiz:

    def __init__(self, no, qn, points,category, op_1, op_2, op_3, op_4, answer):
        self.no = no
        self.qn = qn
        self.points = points
        self.category = category
        self.op_1 = op_1
        self.op_2 = op_2
        self.op_3 = op_3
        self.op_4 = op_4
        self.answer = answer

    def to_dict(self):
        """
        Convert Quiz object to dictionary representation for Firebase or other use cases.
        """
        return {
            'no': self.no,
            'qn': self.qn,
            'points': self.points,
            'category': self.category,
            'op_1': self.op_1,
            'op_2': self.op_2,
            'op_3': self.op_3,
            'op_4': self.op_4,
            'answer': self.answer
        }

    @classmethod
    def from_dict(cls, dict_data):
        """
        Create a Quiz object from a dictionary.
        """
        if isinstance(dict_data, str):
            dict_data = json.loads(dict_data)
        return cls(
            no=dict_data['no'],
            qn=dict_data['qn'],
            points=dict_data['points'],
            category=dict_data['category'],
            op_1=dict_data['op_1'],
            op_2=dict_data['op_2'],
            op_3=dict_data['op_3'],
            op_4=dict_data['op_4'],
            answer=dict_data['answer']
        )
