# -*-coding:utf-8-*-
# coding:utf-8

import jieba
import json
import shutil

import os
class_num = 0
vocal_num = {}



def count_class_num(class_path):
    # os.getcwd()
    classes = os.listdir(class_path)
    # print(classes)
    class_num = len(classes)
    return class_num


class_num = count_class_num("D:\MyDownloads\SogouC.mini\SogouC.mini/Sample")


def pre_gather(essay_path):
    datalist = []
    essays = os.listdir(essay_path)
    for i in essays:
        if os.path.splitext(i)[1] == '.txt':
            datalist.append(i)
    # print(datalist)
    # input all txt names into data list
    out_fp = open(essay_path + '/conclude/conclude.txt', 'w')
    for name in datalist:
        print(name)
        data_path = essay_path + "/" + name
        for line in open(data_path):
            out_fp.writelines(line)
    out_fp.close()


def pre_process(essay_path, stop_word_path, c_name):
    vocal_count = {}
    fp_conclude = open(essay_path + '/conclude/conclude.txt', "r")
    essay = fp_conclude.read()
    vocabulary = jieba.lcut(essay)
    vocal_num.update({c_name: len(vocabulary)})
    stopwords = open(stop_word_path+"/ChineseStopWords.txt", "r")
    stop_list = [i[0:-1] for i in stopwords]
    # print(set(stop_list))
    vocabulary_name = list(set(vocabulary).difference(stop_list))
    for vocal in vocabulary_name:
        count = 0
        for v in vocabulary:
            if v == vocal:
                count += 1
        vocal_count.update({vocal: count})
    return vocal_count


def get_whole_dict(stop_words_path):
    vocal_num_dict = {}
    class_list = os.listdir(stop_words_path+"/Sample")
    print(class_list)
    for name in class_list:
        print(name)
        pre_gather(stop_words_path + "/Sample" + "/" + name)
        class_l = pre_process(stop_words_path + "/Sample" + "/" + name, stop_words_path, name)
        vocal_num_dict.update({name: class_l})
    return vocal_num_dict


def store_in_text(stop_words_path):
    vocal_num_dict = get_whole_dict(stop_words_path)
    try:
        json_str1 = json.dumps(vocal_num_dict)
        with open(stop_words_path+"/result.json", "w", encoding="utf-8") as json_file1:
            json_file1.write(json_str1)
        json_str2 = json.dumps(vocal_num)
        with open(stop_words_path+"/result2.json", "w", encoding="utf-8") as json_file2:
            json_file2.write(json_str2)
        return True
    except:
        return False


output = store_in_text("D:\MyDownloads\SogouC.mini\SogouC.mini")
print("the result of store training results is:")
print(output)





