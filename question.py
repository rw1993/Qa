# -*- coding:utf-8 -*-

class Question(object):
    TRAINING = 0
    TEST = 1
    
    @property
    def correct_ans_content(self):
        index_map = {'A':0, 'B':1, 'C':2, 'D':3}
        if not self.correct_ans:
            return 
        index = index_map[self.correct_ans]
        return self.answers[index]


    def __init__(self, id_, question, answers, c_ans=None):
        self.id = id_
        self.question = question
        self.answers = answers
        self.correct_ans = c_ans

    @classmethod
    def load_from_training_set(cls):
        return cls.load_from_set("training_set.tsv", cls.TRAINING)

    @classmethod
    def load_from_test_set(cls):
        return cls.load_from_set("validation_set.tsv", cls.TEST)

    @classmethod
    def training_get(cls, question):
        id_ = question[0]
        q = question[1]
        c_ans = question[2]
        answers = question[3:]
        return cls(id_, q, answers, c_ans)

    @classmethod
    def test_get(cls, question):
        id_ = question[0]
        q = question[1]
        answers = question[2:]
        return cls(id_, q, answers)

    @classmethod
    def load_from_set(cls, string, flag):
        with open(string, "r") as f:
            lines = [line[:-1] for line in f.readlines()]
            questions = [line[:-1].split("\t") for line in lines[1:]]
            if cls.TRAINING == flag:
                return [cls.training_get(question) for question in questions]
            else:
                return [cls.test_get(question) for question in questions]


if __name__ == "__main__":
    qs = Question.load_from_training_set()
    ts = Question.load_from_test_set()
