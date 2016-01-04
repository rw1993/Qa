# -*- coding:utf-8 -*-
from whoosh.index import create_in
from whoosh.fields import *
import os
from question import *
from whoosh.qparser import QueryParser
from sts import *
import pickle
from build_guesser import get_feature
from nltk.corpus import stopwords

stop_words = stopwords.words("english")

f = open("cls", "rb")
guesser = pickle.load(f)


def guess(q):
    feature = get_feature(q)
    answer = guesser.predict([feature])[0]
    return Question.N_A_MAP[answer]


def build_ix():
    schema = Schema(index=TEXT(stored=True),
                    question=TEXT(stored=True),
                    id=TEXT(stored=True),
                    correct_answer=TEXT(stored=True))
    if not os.path.exists("index"):
        os.mkdir("index")
    ix = create_in("index", schema)
    writer = ix.writer()
    def build_ix_q(q):
        index = q.question + q.correct_answer_content
        id = q.id
        correct_answer = q.correct_answer_content
        writer.add_document(index=index,
                            id=id,
                            correct_answer=correct_answer)
    map(build_ix_q, questions_with_answer)
    writer.commit()
    return ix

def search_answer():
    ix = build_ix()
    ts = questions_without_answer
    with ix.searcher() as searcher:
        def find_question(t):
            try:
                answers = t.answers
                def find_answer(answer):
                    answer = answer.split()
                    answer = filter(lambda x:x not in stop_words, answer)
                    def find_a(a):
                        query = QueryParser("index", ix.schema).parse(a)
                        results = searcher.search(query)
                        return results
                    results = []
                    for a in answer:
                        results += find_a(a)
                    return set(results)
                rs = map(find_answer, answers)
                lens = map(len, rs)
                max_len = max(lens)
                if max_len == 0:
                    return guess(t)
                else:
                    index = lens.index(max_len)
                    return Question.N_A_MAP[index]
            except:
                return guess(t)
        
        for t in ts:
            ans = find_question(t)
            print t.id+","+ans


if __name__ == '__main__':
    #ts = questions_without_answer
    #print guess(ts[0])
    #print stop_words
    search_answer()
