# -*- coding:utf-8 -*-
from question import *
from sklearn.naive_bayes import MultinomialNB as Cls

def get_feature(q):

    rt = map(len, q.answers)
    max_lenth = max(rt)
    min_lenth = min(rt)
    if max_lenth - min_lenth == 0:
        return [0, 0, 0, 0]
    rt = map(float, rt)
    max_lenth = float(max_lenth)
    min_lenth = float(min_lenth)
    def normalize(r):
        return (r - min_lenth) / (max_lenth - min_lenth)
    return map(normalize, rt)


def train_guess():
    qs = questions_with_answer
    Ys = [Question.A_N_MAP[q.correct_answer] for q in qs]
    Xs = [get_feature(q) for q in qs]
    cls = Cls()
    cls.fit(Xs, Ys)
    with open("cls", "wb") as f:
        import pickle
        pickle.dump(cls, f)

if __name__ == '__main__':
    train_guess()
