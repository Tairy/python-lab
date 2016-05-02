#coding=utf-8
from numpy import *
import jieba
import codecs

def levenshtein(source, dest):
    '''Return the levenshteiin distance between source and dest'''
    row_len = len(source) + 1
    col_len = len(dest) + 1

    if row_len == 1 or col_len == 1:
        return max(row_len, col_len)

    matrix = [[col+row for col in range(col_len)] for row in range(row_len)]

    for row in xrange(1, row_len):
        for col in xrange(1, col_len):
            cost = 0 if source[row - 1] == dest[col - 1] else 1

            deletion = matrix[row-1][col] + 1
            insertion = matrix[row][col-1] + 1
            substitution = matrix[row-1][col-1] + cost

            matrix[row][col] = min(deletion, insertion, substitution)

    return matrix[row_len-1][col_len-1]

def load_data_set(file_path):
    data_set = []
    file = codecs.open(file_path, "r", encoding="UTF-8")
    for line in file.readlines():
        cur_line = line.strip()
        data_set.append(cur_line)
    return data_set

def rand_cent(dataSet, k):
    centroids = []
    length = len(dataSet)
    rand_sets = random.rand(k)
    for k in rand_sets:
        centroids.append(dataSet[int(length * k)])

    return centroids

def k_means(data_set, k, centroids):
    m = len(data_set)
    cluster_assment = mat(zeros((m,2)))

    cluster_changed = True
    while cluster_changed:
        cluster_changed = False
        for i in range(m):
            min_dist = inf
            min_index = -1
            for j in range(k):
                ldist = levenshtein(centroids[j], data_set[i])
                if ldist < min_dist:
                    min_dist = ldist
                    min_index = j
            if(cluster_assment[i, 0] != min_index):
                cluster_changed = True
            cluster_assment[i] = min_index, min_dist**2
    return cluster_assment

def main():
    data_set = load_data_set("../data/tag_name.txt")
    centroids = load_data_set("../data/1_stop_words.txt")
    target_file = codecs.open("../data/2_bad_tags.txt", "w+", encoding="UTF-8")
    clust_assing = k_means(data_set, 22, centroids)
    for i in range(len(clust_assing)):
        # print int(clust_assing[i, 0])
        if(int(clust_assing[i, 0]) > 0):
            target_file.write (data_set[i] + "\n")
            print data_set[i].encode("utf-8")
            print centroids[int(clust_assing[i, 0])].encode("utf-8")
    # print rand_cent(data_set, 9)
    # dataMat = mat(loadDataSet('testSet.txt'))
    # myCentroids, clustAssing= kMeans(dataMat,4)
    # print myCentroids
    # show(dataMat, 4, myCentroids, clustAssing)

if __name__ == '__main__':
    main()
