#!usr/bin/env python
#coding=utf-8

import numpy as np
import mysql.connector
from sklearn import neighbors
from sklearn.cross_validation import KFold
import re
import pickle
import os.path
import jieba

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.0.10.211',
                              database='segmentfault')


code_match = re.compile('<pre>(.*?)</pre>', 
                        re.MULTILINE|re.DOTALL)

link_match = re.compile('<a href="http.*?".*?>(.*?)</a>',
                        re.MULTILINE|re.DOTALL)

image_match = re.compile('<img src=*?>',
                        re.MULTILINE|re.DOTALL)


def extract_feature_from_body(s):
  num_code_lines = 0
  link_count_in_code = 0
  code_free_s = s
  image_count = 0
  word_count = 0
  # period_count = 0

  striped_tags_str = re.sub(r'</?\w+[^>]*>','',s)
  cuted_list = jieba.cut(striped_tags_str, cut_all=False)
  word_list = [word.strip() for word in cuted_list if len(word.encode('utf-8')) > 3]
  word_count = len(word_list)

  for match_str in code_match.findall(s):
    num_code_lines += match_str.count('\n')
    code_free_s = code_match.sub("", code_free_s)
    link_count_in_code += len(link_match.findall(match_str))

  links = link_match.findall(s)
  link_count = len(links)
  link_count -= link_count_in_code

  images = image_match.findall(s)
  image_count = len(images)


  # period_count = s.count(u'。')

  return [num_code_lines, link_count, word_count]

try:
  if not os.path.exists("knn.dat"):
    cursor = cnx.cursor()
    cursor.execute("SELECT id, question_id, votes, parsed_text ,created FROM answer WHERE status <> 10")
    Y = []
    X = []

    for (id, question_id, votes, parsed_text ,created) in cursor:
      Y.append(int(votes) > 0)
      X.append(extract_feature_from_body(parsed_text))

    X = np.asarray(X)
    Y = np.asarray(Y)

    knn = neighbors.KNeighborsClassifier(n_neighbors=90)
    knn.fit(X, Y)
    pickle.dump(knn, open("knn.dat", "w"))
  else:
    knn = pickle.load(open("knn.dat", "r"))

    sample = [2, 0, 100]
    print knn.predict(sample)
    print knn.predict_proba(sample)

    ## These code is for test score of method
    # cursor = cnx.cursor()
    # cursor.execute("SELECT id, question_id, votes, parsed_text ,created FROM answer WHERE status <> 10")
    # Y = []
    # X = []

    # for (id, question_id, votes, parsed_text ,created) in cursor:
    #   Y.append(int(votes) > 0)
    #   X.append(extract_feature_from_body(parsed_text))

    # X = np.asarray(X)
    # Y = np.asarray(Y)

    # test_scores = []
    # cv = KFold(n=len(X), n_folds=10)

    # for train, test in cv:
    #   X_train , Y_train = X[train], Y[train]
    #   X_test, Y_test = X[test], Y[test]

    #   # clf = neighbors.KNeighborsClassifier(n_neighbors=5)
    #   knn.fit(X_train, Y_train)

    #   test_score = knn.score(X_test, Y_test)

    #   test_scores.append(test_score)

    # print np.std(test_scores)
    # print np.mean(test_scores)


finally:
  cnx.close()