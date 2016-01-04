# -*- coding:utf-8 -*-

class Question(object):
    TRAINING = 0
    TEST = 1
    A_N_MAP = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    N_A_MAP = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    
    @property
    def correct_answer_content(self):
        if not self.correct_answer:
            return 
        index = self.A_N_MAP[self.correct_answer]
        return self.answers[index]
    
    def decode(self, attr):
        try:
            return attr.decode("utf8")
        except:
            return u""

    @property
    def id(self):
        return self.decode(self._id)

    @property
    def question(self):
        return self.decode(self._question)

    @property
    def answers(self):
        return map(self.decode, self._answers)

    @property
    def correct_answer(self):
        return self.decode(self._correct_ans)

    def __init__(self, id_, question, answers, c_ans=None):
        self._id = id_
        self._question = question
        self._answers = answers
        self._correct_ans = c_ans

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


questions_with_answer = Question.load_from_training_set()


questions_without_answer = Question.load_from_test_set()


if __name__ == "__main__":
    q = questions_with_answer[0]
    print q.question
    print q.answers
