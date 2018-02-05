# encoding:utf-8
import os
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected, flatten
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import batch_normalization
from tflearn.layers.estimator import regression
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt

TRAIN_SET_PATH = "/Users/tairy/Documents/Working/python-lab/tensorflow/train_splits/"
VALID_SET_PATH = "/Users/tairy/Documents/Working/python-lab/tensorflow/valid_splits/"
MODEL_NAME = "taobao_captcha"
MODEL_PATH = "/Users/tairy/Documents/Working/python-lab/tensorflow/model/"
LOG_PATH = "/Users/tairy/Documents/Working/python-lab/tensorflow/tflog/"
CHECK_POINT = "/Users/tairy/Documents/Working/python-lab/tensorflow/check_point/"
PREDICT_PATH = "/Users/tairy/Documents/Working/python-lab/tensorflow/predict_splits/"
IMAGE_WIDTH = 20
IMAGE_HEIGHT = 20
CODE_LEN = 1
MAX_CHAR = 10


def show_image(image, gray=False):
    if gray:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(image)
    plt.axis("off")
    plt.show()


def load_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def convert_to_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray


def adaptive_threshold(image):
    image = cv2.adaptiveThreshold(image, 100, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 0)
    return image


def text2vec(text):
    vec = np.zeros(CODE_LEN * MAX_CHAR)
    for i, c in enumerate(text):
        char = ord(c)
        vec[i * MAX_CHAR + char - ord('0')] = 1
    return vec


def vec2text(vec):
    text = ''
    max_value = []
    for pos in range(CODE_LEN):
        max_value.append(np.max(vec[pos * MAX_CHAR:(pos + 1) * MAX_CHAR]))

    for i, v in enumerate(vec):
        if v == max_value[int(i / MAX_CHAR)]:
            text += chr(i % MAX_CHAR + ord('0'))
    return text


def load_batch(path):
    files = []
    for item in os.walk(path):
        files = item[2]
        break
    amount = len(files)
    print("[+]开始载入样本-%s" % (path))
    x_batch = np.zeros([amount, IMAGE_HEIGHT, IMAGE_WIDTH])
    y_batch = np.zeros([amount, MAX_CHAR * CODE_LEN])

    for i, filename in enumerate(files):
        if '.DS_Store' == filename:
            continue
        text = filename.split('.')[0]
        text = text.split('-')[-1]
        y_batch[i, :] = text2vec(text)
        filepath = os.path.join(path, filename)
        # print(filepath)
        image = load_image(filepath)
        image = convert_to_gray(image)
        image = adaptive_threshold(image)
        x_batch[i, :] = image
    print("[+]成功载入%s个样本" % (amount))
    x_batch = x_batch.reshape([-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])
    return x_batch, y_batch


def load_predict(path):
    files = []
    # for item in os.walk(path):
        # files = item[2]
        # break
    files = ['1-0-0.jpeg','1-1-1.jpeg','1-2-2.jpeg','1-3-3.jpeg', '1-4-4.jpeg', '1-5-5.jpeg']
    amount = len(files)
    print("[+]开始载入样本-%s" % (path))
    x_batch = np.zeros([amount, IMAGE_HEIGHT, IMAGE_WIDTH])
    for i, filename in enumerate(files):
        if '.DS_Store' == filename:
            continue
        filepath = os.path.join(path, filename)
        image = load_image(filepath)
        image = convert_to_gray(image)
        image = adaptive_threshold(image)
        x_batch[i, :] = image
    print("[+]成功载入%s个样本" % (amount))
    x_batch = x_batch.reshape([-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])
    return x_batch


def cnn():
    network = input_data(shape=[None, IMAGE_HEIGHT, IMAGE_WIDTH, 1], name='input')
    network = conv_2d(network, 8, 3, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = batch_normalization(network)
    network = conv_2d(network, 16, 3, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = batch_normalization(network)
    network = conv_2d(network, 16, 3, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = batch_normalization(network)
    network = fully_connected(network, 256, activation='tanh')
    network = dropout(network, 0.8)
    network = fully_connected(network, 256, activation='tanh')
    network = dropout(network, 0.8)
    network = fully_connected(network, CODE_LEN * MAX_CHAR, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy', name='target')
    return network


def train():
    print('[+]加载训练集')
    train_X, train_Y = load_batch(TRAIN_SET_PATH)
    print('[+]加载验证集')
    valid_X, valid_Y = load_batch(VALID_SET_PATH)
    model = tflearn.DNN(cnn(), tensorboard_verbose=0, checkpoint_path=None,
                        best_checkpoint_path=CHECK_POINT, max_checkpoints=100,
                        tensorboard_dir=LOG_PATH)
    model.fit({'input': train_X}, {'target': train_Y}, n_epoch=200,
              validation_set=({'input': valid_X}, {'target': valid_Y}),
              snapshot_step=100, show_metric=True, run_id=MODEL_NAME, )
    model.save(MODEL_NAME)


def test():
    print('[+]加载验证集')
    valid_X, valid_Y = load_batch(VALID_SET_PATH)
    model_test = tflearn.DNN(cnn(), tensorboard_verbose=0, checkpoint_path=None,
                             best_checkpoint_path=CHECK_POINT,
                             max_checkpoints=100, tensorboard_dir=LOG_PATH)
    model_test.load('/Users/tairy/Documents/Working/python-lab/tensorflow/taobao_captcha')
    result = model_test.predict(valid_X)
    for i in range(result.shape[0]):
        answer = vec2text(valid_Y[i])
        predict = vec2text(result[i])
        print('[+]正确结果:%s || 预测结果:%s' % (answer, predict))
        if answer != predict:
            print(">>>!<<<")
            show_image(valid_X[i].reshape([IMAGE_HEIGHT, IMAGE_WIDTH]), gray=True)


def predict():
    print('[+]加载预测集')
    predict_X = load_predict(PREDICT_PATH)
    model_predict = tflearn.DNN(cnn(), tensorboard_verbose=0, checkpoint_path=None,
                                best_checkpoint_path=CHECK_POINT,
                                max_checkpoints=100, tensorboard_dir=LOG_PATH)
    model_predict.load('/Users/tairy/Documents/Working/python-lab/tensorflow/taobao_captcha')
    result = model_predict.predict(predict_X)
    for i in range(result.shape[0]):
        predict = vec2text(result[i])
        print('[+]预测结果:%s' % predict)
        print(">>>!<<<")
        # show_image(predict_X[i].reshape([IMAGE_HEIGHT, IMAGE_WIDTH]), gray=True)


if __name__ == '__main__':
    predict()
    # test()
    # train()
