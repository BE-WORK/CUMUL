# -*- coding:utf-8 -*-
import os
import csv
import numpy as np
from scipy import interpolate
from sklearn import preprocessing


def extract_features(csv_file):
    """
    此函数从单位csv文件中计算出特征。
    :param csv_file:csv文件的路径。
    :return:返回一个特征列表，元素的类型为float。
    """
    features = []  # 特征序列
    n_sample = 100  # 采样个数
    with open(csv_file, 'rb') as length_file:
        csv_reader = csv.reader(length_file)
        in_lengths = []  # “接收”数据包Length字段序列
        out_lengths = []  # “发送”数据包Length字段序列
        lengths = []  # “双向”数据包Length字段序列
        for length in csv_reader:
            length = int(length[0])
            if length > 0:
                in_lengths.append(length)
            else:
                out_lengths.append(length)
            lengths.append(length)
        features.append(len(in_lengths))  # N_in
        features.append(len(out_lengths))  # N_out
        features.append(sum(in_lengths))  # S_in
        features.append(abs(sum(out_lengths)))  # S_out
        cumulative_representation = [0.]  # 这里的元素表示的是论文中的ci
        cumulative_sum = 0.
        for length in lengths:
            cumulative_sum += length
            cumulative_representation.append(cumulative_sum)
        x = np.linspace(start=0, stop=len(cumulative_representation), num=len(cumulative_representation),
                        endpoint=False)
        cumulative_representation = np.array(cumulative_representation, dtype=float)
        linear_piecewise_func = interpolate.interp1d(x, cumulative_representation)  # 获取分段线性插值函数
        stepwise = float(len(cumulative_representation) - 1) / 100.  # 求出步长
        for i in range(n_sample - 1):
            features.append(float(linear_piecewise_func(stepwise * (i + 1))))
        features.append(cumulative_representation[-1])
    return features


def extract(path_root, k, partition_num):
    """
    此函数将所有计算所有训练集和测试集的特征信息。
    :param path_root: 数据集所在的根目录。
    :param k: 第k次交叉验证。
    :param partition_num: 指明以第partition_num个子集作为测试集。
    :return: none
    """
    path_length = path_root + '/data_packet_length'
    path_cv_k = path_root + '/tmp/cross_validation_' + str(k) + '.csv'
    path_train_features = path_root + '/tmp/train_features.csv'
    path_test_features = path_root + '/tmp/test_features.csv'
    path_train_features_scaled = path_root + '/tmp/train_features_scaled.csv'
    path_test_features_scaled = path_root + '/tmp/test_features_scaled.csv'

    train_mark = []  # 标记训练集
    test_mark = []  # 标记测试集
    with open(path_cv_k, 'rb') as split_file:
        csv_reader = csv.reader(split_file)
        for line in csv_reader:
            if partition_num == int(line[0][-1]):
                for f in line[1:]:
                    test_mark.append(f)
            else:
                for f in line[1:]:
                    train_mark.append(f)

    train_features = []
    train_label = []
    test_features = []
    test_label = []
    goods = os.listdir(path_length)
    for g in goods:
        pages = os.listdir(path_length + '/' + g)
        for p in pages:
            fetches = os.listdir(path_length + '/' + g + '/' + p)
            for f in fetches:
                instance_num = f.split('-')[-1].split('.')[0]
                page_name = '-'.join(f.split('-')[:-1])
                f_path = path_length + '/' + g + '/' + p + '/' + f
                features = extract_features(f_path)
                if instance_num in train_mark:
                    train_features.append(features)
                    train_label.append(page_name)
                else:
                    test_features.append(features)
                    test_label.append(page_name)

    # 将标准化之前的特征写入文件
    with open(path_train_features, 'wb') as train_features_file:
        csv_writer = csv.writer(train_features_file)
        for i, features in enumerate(train_features):
            csv_writer.writerow(map(str, features) + [train_label[i]])
    with open(path_test_features, 'wb') as test_features_file:
        csv_writer = csv.writer(test_features_file)
        for i, features in enumerate(test_features):
            csv_writer.writerow(map(str, features) + [test_label[i]])

    # 标准化
    scaler = preprocessing.MinMaxScaler()
    train_features = scaler.fit_transform(np.array(train_features, dtype=float)).tolist()
    test_features = scaler.transform(np.array(test_features, dtype=float)).tolist()

    # 将标准化之后的特征写入文件
    with open(path_train_features_scaled, 'wb') as train_scaled_file:
        csv_writer = csv.writer(train_scaled_file)
        for i, features in enumerate(train_features):
            csv_writer.writerow(features + [train_label[i]])
    with open(path_test_features_scaled, 'wb') as test_scaled_file:
        csv_writer = csv.writer(test_scaled_file)
        for i, features in enumerate(test_features):
            csv_writer.writerow(features + [test_label[i]])


def main():
    path = raw_input('Enter the root path of your data: ')
    if path == '':
        path = 'C:/ScriptData/CUMUL_SVM'
    elif path.find('\\') != -1:  # 转换路径格式
        path = path.replace('\\', '/')
    extract(path, k=1, partition_num=1)


if __name__ == '__main__':
    main()
