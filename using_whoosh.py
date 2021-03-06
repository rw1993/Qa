# -*- coding:utf-8 -*-
from whoosh.index import create_in
from whoosh.fields import *
import os
from question import Question
from whoosh.qparser import QueryParser
from sklearn.cluster import KMeans

def build_ix(questions):
    if not os.path.exists('index'):
        os.mkdir('index')

    schema = Schema(question=TEXT(stored=True),
                    ans=TEXT(stored=True),
                    id_=TEXT(stored=True))

    ix = create_in('index', schema)
    
    writer = ix.writer()

    for q in questions:
        ix_write(q, writer)
    
    writer.commit()
    return ix


def ix_write(q, writer):
    question = q.question.decode("utf8")
    ans = q.correct_ans_content.decode("utf8")
    id_ = str(q.id).decode("utf8")
    writer.add_document(question=question,
                        ans=ans,
                        id_=id_)


def get_answers(questions, ix):
    print "id,correctAnswer"

    for q in questions:
        get_ans(q, ix)


def chinese_student(q):
    # This function is inspired by Chinese stuendets
    # Choose shortest One if ohter answer are long
    # Choose B if two answers long two answers are short
    # Here we can use kmeans where k = 2 and numbers of input are 4
    answers = q.answers
    lengths = [len(answer) for answer in answers]
    max_length = max(lengths)
    min_length = min(lengths)
    if max_length - min_length == 0:
        print (q.id, "C")
        return
    l_range = float(max_length - min_length)
    def normalize(length):
        length = float(length)
        return (length - min_length) / l_range
    lengths = [normalize(length) for length in lengths]
    lengths = map(lambda length:[length], lengths)
    c = KMeans(n_clusters=2)
    result = c.fit_predict(lengths)
    result = list(result)
    if sum(result) == 2:
        print (q.id, "B")
    else:
        if sum(result) == 3:
            index = result.index(0)
        else:
            index = result.index(1)
        a_map = {0:'A', 1:'B', 2:'C', 3:'D'}
        ans = a_map[index]
        print (q.id, ans)
    print (q.id ,"C")


def get_ans(q, ix):
    with ix.searcher() as searcher:
        question = q.question.decode("utf-8")
        query = QueryParser("question", ix.schema).parse(question)
        rs = searcher.search(query)
        if not rs:
            #chinese_student(q)
            pass
        else:
            ans = search_ans(rs, q)
            if not ans:
                #chinese_student(q)
                pass
            else:
                print q.id, ans


def search_ans(rs, q):
    try:
        a_map = {0:'A',1:'B',2:'C',3:'D'}
        index_name = str(q.id)
        if not os.path.exists(index_name):
            os.mkdir(index_name)
        schema = Schema(ans=TEXT(stored=True))
        ix = create_in(index_name, schema)
        writer = ix.writer()
        answers = [answer.decode("utf8") for answer in q.answers]
        for answer in answers:
            writer.add_document(ans=answer)
        writer.commit()
        with ix.searcher() as searcher:
            for r in rs:
                question = r['ans'].decode("utf8")
                query = QueryParser('ans', ix.schema).parse(question)
                results = searcher.search(query)
                if results:
                    ans = answers.index(results[0]['ans'])
                    ans = a_map[ans]
                    return ans
    except:
        return 



if __name__ == '__main__':
    questions = Question.load_from_training_set()
    ix = build_ix(questions)
    questions = Question.load_from_test_set()
    get_answers(questions, ix)

