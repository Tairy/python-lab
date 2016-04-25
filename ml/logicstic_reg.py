#!usr/bin/env python
#coding=utf-8

import numpy as np
import mysql.connector
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve, roc_curve, auc
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
  if not os.path.exists("logreg.dat"):
    cursor = cnx.cursor()
    cursor.execute("SELECT id, question_id, votes, parsed_text ,created FROM answer WHERE status <> 10")
    Y = []
    X = []

    for (id, question_id, votes, parsed_text ,created) in cursor:
      Y.append(int(votes) > 0)
      X.append(extract_feature_from_body(parsed_text))

    X = np.asarray(X)
    Y = np.asarray(Y)

    clf = LogisticRegression()
    clf.fit(X, Y)
    pickle.dump(clf, open("logreg.dat", "w"))
  else:
    clf = pickle.load(open("logreg.dat", "r"))
    # print clf
    # print(np.exp(clf.intercept_), np.exp(clf.coef_.ravel()))
    sample = [2, 0, 80]
    print clf.predict(sample)
    print clf.predict_proba(sample)

    ## These code is for test score of method
    # test_scores = []
    # train_scores = []

    # train_errors = []
    # test_errors = []

    # scores = []
    # roc_scores = []
    # fprs, tprs = [], []

    # pr_scores = []
    # precisions, recalls, thresholds = [], [], []

    # cv = KFold(n=len(X), n_folds=10)

    # for train, test in cv:
    #   X_train , Y_train = X[train], Y[train]
    #   X_test, Y_test = X[test], Y[test]

    #   clf.fit(X_train, Y_train)

    #   train_score = clf.score(X_train, Y_train)
    #   test_score = clf.score(X_test, Y_test)

    #   train_errors.append(1 - train_score)
    #   test_errors.append(1 - test_score)

    #   scores.append(test_score)
    #   proba = clf.predict_proba(X_test)

    #   label_idx = 1
    #   fpr, tpr, roc_thresholds = roc_curve(Y_test, proba[:, label_idx])
    #   precision, recall, pr_thresholds = precision_recall_curve(Y_test, proba[:, label_idx])

    #   roc_scores.append(auc(fpr, tpr))

    #   fprs.append(fpr)
    #   tprs.append(tpr)

    #   pr_scores.append(auc(recall, precision))
    #   precisions.append(precision)
    #   recalls.append(recall)
    #   thresholds.append(pr_thresholds)

      # print(classification_report(Y_test, proba[:, label_idx] > 0.63, target_names=['not accepted', 'accepted']))
    # print np.mean(train_errors), np.mean(test_errors)


    # print np.std(test_scores)
    # print np.mean(test_scores)

finally:
  cnx.close()