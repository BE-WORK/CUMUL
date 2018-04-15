# -*- coding:utf-8 -*-
import os
import csv


def extract_packet_length(path_root):
    """
    此函数从csv文件中抽取数据包Length字段。
    :param path_root: 数据的根目录。
    :return: none
    """
    path_csv = path_root + '/data_csv'  # 存放csv文件的路径，csv文件的格式是包含7列信息，第6列是数据包length字段
    path_packet_length = path_root + '/data_packet_length'
    if not os.path.exists(path_packet_length):  # 此文件夹的目录将和path_csv目录一致
        os.mkdir(path_packet_length)
    my_ipv4 = '172.29.23.168'

    goods = os.listdir(path_csv)
    for g in goods:  # 遍历第一层目录
        if not os.path.exists(path_packet_length + '/' + g):
            os.mkdir(path_packet_length + '/' + g)
        pages = os.listdir(path_csv + '/' + g)
        for p in pages:  # 遍历第二层目录
            if not os.path.exists(path_packet_length + '/' + g + '/' + p):
                os.mkdir(path_packet_length + '/' + g + '/' + p)
            fetches = os.listdir(path_csv + '/' + g + '/' + p)
            for f in fetches:  # 遍历第三层目录
                with open(path_csv + '/' + g + '/' + p + '/' + f, 'rb') as file_src:
                    csv_reader = csv.reader(file_src)
                    with open(path_packet_length + '/' + g + '/' + p + '/' + f, 'w') as file_dst:
                        for line in csv_reader:  # 抽取数据包Length字段
                            if line[2] == my_ipv4:
                                file_dst.write('-' + line[5] + '\n')
                            else:
                                file_dst.write(line[5] + '\n')


def main():
    path = raw_input('Enter the root path of your data: ')
    if path.find('\\'):  # 转换路径格式
        path = path.replace('\\', '/')
    if path == '':
        extract_packet_length(path_root='C:/ScriptData/CUMUL_SVM')
    else:
        extract_packet_length(path)


if __name__ == '__main__':
    main()
