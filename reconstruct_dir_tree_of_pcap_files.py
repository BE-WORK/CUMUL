# -*- coding: utf-8 -*-

import os
import shutil


def create_folder_for_each_page(path_root):
    """
    此函数会重新组织pcap数据的文件目录树。在每一类商品的流量文件（每个网页获取次数是20次）存放在一个文件夹的情况下使用此脚本，
    脚本会在商品文件夹下若干个子文件夹，每个子文件夹代表一个网页，里面存放同一个网页的多次获取产生的流量文件。
    :return: 无返回值。
    :param path_root: 数据集所在的根目录。
    :return: none
    """
    path_pcap = path_root + '/data_pcap'
    goods = os.listdir(path_pcap)
    for g in goods:  # 遍历一级目录
        cnt = 0
        files = os.listdir(path_pcap + '/' + g)
        for f in files:
            if cnt == 0:  # 创建子文件夹
                sub_folder = '-'.join(f.split('-')[0:2])
                if not os.path.exists(path_pcap + '/' + g + '/' + sub_folder):
                    os.mkdir(path_pcap + '/' + g + '/' + sub_folder)
            shutil.move(path_pcap + '/' + g + '/' + f, path_pcap + '/' + g + '/' + sub_folder)
            cnt += 1
            if cnt == 20:  # 每个网页都是20次获取
                cnt = 0


def main():
    path = raw_input('Enter the root path of your data: ')
    if path.find('\\'):  # 转换路径格式
        path = path.replace('\\', '/')
    if path == '':
        create_folder_for_each_page(path_root='C:/ScriptData/CUMUL_SVM')
    else:
        create_folder_for_each_page(path_root=path)


if __name__ == '__main__':
    main()