# -*- coding:utf-8 -*-
from whoosh.index import create_in
from whoosh.fields import *
import os
from question import Question
from whoosh.qparser import QueryParser
from sklearn.cluster import KMeans
from sts import *


n_a_map = {0:"A", 1:"B", 2:"C", 3:"D"}
a_n_map = {"A":0, "B":1, "C":2, "D":3}

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
        print q.id, "C"
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
        print q.id, "B"
    else:
        if sum(result) == 3:
            index = result.index(0)
        else:
            index = result.index(1)
        a_map = {0:'A', 1:'B', 2:'C', 3:'D'}
        ans = a_map[index]
        print q.id, ans
    print q.id ,"C"


def build_ix(questions):
    if not os.path.exists("index"):
        os.mkdir("index")

    schema = Schema(title=TEXT(stored=True),
                    question=TEXT(stored=True))

    ix = create_in("index", schema)

    writer = ix.writer()
    for q in questions:
        write_ix(q, writer)
    writer.commit()

    return ix


def write_ix(q, writer):
    title = q.correct_ans_content.decode("utf8")
    question = q.question.decode("utf8")
    writer.add_document(title=title,
                        question=question)


def get_answers(questions, ix):
    with ix.searcher() as searcher:
        for q in questions:
            try:
                get_answer(q, ix, searcher)
            except:
                chinese_student(q)


def get_answer(q, ix, searcher):
    answers = [answer.decode("utf8") for answer in q.answers]
    
    def query_from_answer(answer):
        #search answer from right answer
        query = QueryParser("question", ix.schema).parse(answer)
        results = searcher.search(query)
        return results[0] if results else None

    questions = map(query_from_answer, answers)
    q_question = q.question.decode("utf8")
    def compare_question(question):
        if not question:
            return 0
        else:
            # count similarity
            sentences = [question, q_question]
            dics = build_dics(sentences)
            vectors = word_to_dic(sentences, dics)
            sims = map(count_similarity, vectors)
            return sims[0]

    similarities = map(compare_question, questions)
    max_sim = max(similarities)
    if max_sim == 0:
        chinese_student(q)
    else:
        index = similarities.index(max_sim)
        print q.id, n_a_map[index]
    

if __name__ == '__main__':
    questions = Question.load_from_training_set()
    ix = build_ix(questions)
    questions = Question.load_from_test_set()
    get_answers(questions, ix)
