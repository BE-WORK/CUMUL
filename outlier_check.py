# -*- coding:utf-8 -*-
import os
import csv
import numpy as np


def report_outliers(path_root):
    path_packet_length = path_root + '/data_packet_length'

    goods = os.listdir(path_packet_length)
    for g in goods:
        pages = os.listdir(path_packet_length + '/' + g)
        for p in pages:
            fetches = os.listdir(path_packet_length + '/' + g + '/' + p)
            for f in fetches:
                with open(path_packet_length + '/' + g + '/' + p + '/' + f, 'rb') as file_length:
                    csv_reader = csv.reader(file_length)
                    incomes = []  # “接收”数据包Length字段序列
                    for length in csv_reader:
                        length = int(length[0])
                        if length > 0:
                            incomes.append(length)
                    incomes = np.array(incomes, dtype=float)
                    I = incomes.sum()
                    Q1, Q3 = np.percentile(incomes, [25., 75.])
                    if Q1 - 1.5 * (Q3 - Q1) < I < Q3 + 1.5 * (Q3 - Q1):
                        with open('outliers.csv', 'w+') as file_outlier:
                            file_outlier.write(f.split('.')[0] + '\n')


def main():
    path = raw_input('Enter the root path of your data: ')
    if path.find('\\'):  # 转换路径格式
        path = path.replace('\\', '/')
    if path == '':
        report_outliers(path_root='C:/ScriptData/CUMUL_SVM')
    else:
        report_outliers(path)


if __name__ == '__main__':
    main()
