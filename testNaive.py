# -*-coding:utf-8-*-
# coding:utf-8

import json
import jieba
import os


def read_json(path1, path2):
    with open(path1, "r") as file1:
        str1 = file1.read()
        vocal_num_dict = json.loads(str1)
    # print(type(vocal_num_dict))
    # print(vocal_num_dict)
    with open(path2, "r") as file2:
        str2 = file2.read()
        vocal_class_num = json.loads(str2)
    return vocal_num_dict, vocal_class_num


def cal_the_total_num(vocal_class_num):
    total_num = 0
    for i in vocal_class_num:
        total_num += vocal_class_num[i]
    return total_num


def pre_process_test(test_path, stop_words_path):
    fp = open(test_path, "r")
    test_essay = fp.read()
    vocabulary = jieba.lcut(test_essay)
    # print(type(vocabulary))
    fp_stop = open(stop_words_path, "r")
    stop_list = [i[0:-1] for i in fp_stop]
    # print(stop_list)
    test_vocal = [i for i in vocabulary if i not in stop_list]
    fp.close()
    fp_stop.close()
    return test_vocal


def cal_pxc(test_vocal):
    vocal_num_dict, vocal_class_num = read_json("D:\MyDownloads\SogouC.mini\SogouC.mini/result.json",
                                                "D:\MyDownloads\SogouC.mini\SogouC.mini/result2.json")
    total_num = cal_the_total_num(vocal_class_num)
    p_result = {}
    for classes in vocal_class_num:
        p_one_test = 1
        d_num = vocal_class_num[classes]
        vocal = vocal_num_dict[classes]
        for not_in_word in test_vocal:
            if not_in_word not in vocal:
                vocal.update({not_in_word: 1})
                d_num += 1
                total_num += 1
                # print("add 1 word: "+not_in_word)
        for word in test_vocal:
            p = vocal[word]/d_num
            p_one_test = p_one_test * p
        p_xc = p_one_test * (d_num/total_num)
        p_result.update({classes: p_xc})
    return p_result


def compare_pxc(test_vocal):
    p_result = cal_pxc(test_vocal)
    max_p = 0
    class_p_max = ''
    for p in p_result:
        if p_result[p] > max_p:
            max_p = p_result[p]
            class_p_max = p
    return class_p_max


test_path = "D:\MyDownloads\SogouC.mini/test"
test_list = os.listdir(test_path)
test_total_num = len(test_list)
correct_count = 0
for file_name in test_list:
    test_vocal_main = pre_process_test(test_path + "/" + file_name, "D:\MyDownloads\SogouC.mini\SogouC.mini/ChineseStopWords.txt")
    class_result = compare_pxc(test_vocal_main)
    # print(class_result)
    if class_result == file_name[:-5]:
        correct_count += 1
correct_rate = (correct_count/test_total_num)
print(correct_rate)