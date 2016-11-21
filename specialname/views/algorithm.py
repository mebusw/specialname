#!encoding=utf8

from pipe import *
import os


def choose_name_by_character_and_gender(characters, gender):
    data = _read_csv('male_names.txt') if int(gender) == 0 else _read_csv('female_names.txt')
    return _choose_name_by_character(characters.split(',') | select(lambda x: int(x)) | as_list, data)


def _read_csv(filename):
    p = os.path.join(os.path.dirname(__file__), filename)
    with open(p) as f:
        lines = f.readlines()
        lines = lines | select(lambda l: l.split(','))
    return lines | as_list


def _choose_name_by_character(characters, data):
    """
    输入：characters数组用0或1表示每个属性是否选中

    二者相乘并求和(矩阵乘法)可以得到单个字针对所有属性的整体权重
       0------------3 , 4--------->
       名,拼音,权重,音调,honorable,intellectual,elegant,agile,powerful,organized,lucky,precious,artistic,beautiful,reliable,free

    :param characters:
    @return 根据输入选择的按权重排序的汉字列表

    """

    names = data | select(
        lambda d: [d[0], d[1], d[3], sum(map(lambda x, y: int(x) * y, d[4:16], characters))]) | as_list
    ordered = sorted(names, key=lambda n: n[3], reverse=True)
    # print ordered
    return ordered


def _choose_name_word_by_tone(characters, english_name, data):
    """
    中文词组,英文名,英文名,英文名,权重,honorable,intellectual,elegant,agile,powerful,organized,lucky,precious,artistic,beautiful,reliable,free,,,,
    :return:
    """
    names = data | where(lambda d: english_name in d[1:4]) | as_list
    # print names
    return map(lambda n: n[0], names)
