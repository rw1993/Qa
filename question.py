# -*- conding:utf-8 -*-

class Question(object):
    TRAINING = 0
    TEST = 1

    def __init__(self, id_, question, ansers, c_anser=None):
        self.id = id_
        self.question = question
        self.ansers = ansers
        self.correct_anser = c_anser

    @classmethod
    def load_from_training_set(cls, string):
        return cls.load_from_set(string, cls.TRAINING)
    
    @classmethod
    def load_from_test_set(cls, string):
        return cls.load_from_set(string, cls.TEST)

    @classmethod 
    def training_get(cls, question):
        id_ = question[0]
        q = question[1]
        c_anser = question[2]
        ansers = question[3:]
        return cls(id_, q, ansers, c_anser)

    @classmethod 
    def test_get(cls, question):
        id_ = question[0]
        q = question[1]
        ansers = question[2:]
        return cls(id_, q, ansers)

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
    qs = Question.load_from_training_set("training_set.tsv")
