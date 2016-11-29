#!encoding=utf8
import itertools
from pipe import *
import os
from random import random


def _parse_to_int_array(characters):
    return characters.split(',') | select(lambda x: int(x)) | as_list


def _choose_name_by_character_and_gender(characters, gender):
    data = _read_csv('male_names.txt') if int(gender) == 0 else _read_csv('female_names.txt')
    print characters
    return _choose_name_by_character(_parse_to_int_array(characters), data)


def _read_csv(filename):
    p = os.path.join(os.path.dirname(__file__), filename)
    with open(p) as f:
        lines = f.readlines() | select(lambda l: l.split(','))
    return lines | as_list


def _choose_name_by_character(characters, data):
    """
    输入：characters数组用0或1表示每个属性是否选中

    二者相乘并求和(矩阵乘法)可以得到单个字针对所有属性的整体权重
       0------------3 , 4--------->
       名,拼音,权重,音调,honorable,intellectual,elegant,agile,powerful,organized,lucky,precious,artistic,beautiful,reliable,free

    :param characters:
    @return 根据输入选择的按权重排序的汉字列表  [{'汉', 拼音, 音调, 打分}, ...]

    """

    names = data | select(
        lambda d: [d[0], d[1], d[3], sum(map(lambda x, y: int(x) * y, d[4:16], characters))]) | as_list
    ordered = sorted(names, key=lambda n: n[3], reverse=True)
    # print ordered
    return ordered


def _find_existing_name_word(english_name, client_chars=[], data=[]):
    """
    中文词组,英文名,英文名,英文名,权重,honorable,intellectual,elegant,agile,powerful,organized,lucky,precious,artistic,beautiful,reliable,free,,,,
    :return: {'中文二字词组', '拼音组', 音调1, 音调2, 打分}
    """
    names = data | where(lambda d: english_name in d[1:4]) | select(lambda n: (n[0], 'pinyin', 1, 1, 5)) | as_list
    return names


def _filter_chinese_names_by_tones(chinese_family_name, chinese_char_combinations, chinese_word):
    """

    :param chinese_family_name: 中文姓
    :param chinese_char_combinations: 中文字组合
    :param chinese_word: 中文现有词组
    :return: 根据读音平仄进行二次打分
    """
    return [{'刘德华', 'liu de hua'}, {'周润发', 'zhou run fa'}]


def _choose_family_name_by_character(order_client_chars, data):
    """

    :param order_client_chars:
    :return: {'姓', 拼音, 音调, 打分}
    """
    # TODO 姓氏缺性格分数
    rand = int(random() * len(data))
    # return {'申', 'shen', 1, 3}
    d = data[rand]
    return d[0], d[1], d[2], 5


def _mix_chinese_chars(chinese_chars):
    """
    组合单字成为二字词组
    :param chinese_chars: [{'汉', 拼音, 音调, 打分}, ...]
    :return: [{'词组', '拼音组', 音调1, 音调2, 平均分}]
    """
    ### Assume 3 chars to mix
    return [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)] | \
           select(lambda x: [
               (chinese_chars[x[0]][0] + chinese_chars[x[1]][0]),
               (chinese_chars[x[0]][1] + chinese_chars[x[1]][1]),
               (chinese_chars[x[0]][2]),
               (chinese_chars[x[1]][2]),
               ((chinese_chars[x[0]][3] + chinese_chars[x[1]][3]) / 2.0),
           ]) | as_list


def deliver_name(order_client_chars, order_client_gender, english_name=''):
    chinese_chars = _choose_name_by_character_and_gender(order_client_chars, order_client_gender)[
                    0:10]  # TODO itertools.count(5) | take(10) | islice(2,5) | as_list
    chinese_char_combinations = _mix_chinese_chars(chinese_chars)
    chinese_word = _find_existing_name_word(english_name, [], data=_read_csv('name_words.txt'))
    chinese_family_name = _choose_family_name_by_character(order_client_chars, data=_read_csv('family_names.txt'))
    chinese_names = _filter_chinese_names_by_tones(chinese_family_name, chinese_char_combinations, chinese_word)
    return chinese_names
