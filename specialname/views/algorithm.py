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
    中文词组,拼音组,英文名,英文名,英文名,权重,honorable,intellectual,elegant,agile,powerful,organized,lucky,precious,artistic,beautiful,reliable,free,,,,
    :return: {'中文二字词组', '拼音组', 音调1, 音调2, 打分}
    """
    names = data | where(lambda d: english_name != '' and english_name in d[3:7]) | select(
        lambda n: (n[0], n[1], int(n[2]), int(n[3]), 5)) | as_list
    return names


def _filter_chinese_names_by_tones(chinese_family_name, chinese_char_combinations, chinese_word):
    """

    :param chinese_family_name: 中文姓 ('姓', '拼音', 音调, 打分)
    :param chinese_char_combinations: 中文字组合 ('组合', '拼音', 音调1, 音调2, 打分)
    :param chinese_word: 中文现有词组 ('词组', '拼音', 音调1, 音调2, 打分)

    perfer=2: 平仄平,平平平,仄仄平,仄平平
    normal=1: ~
    refuse=0: 仄仄仄

    :return: 根据三个汉字的音调平仄进行二次打分rating 0~2
    """

    def pingze_rating(ccc):
        rating = 1
        are_ping = map(lambda t: t in (1, 2), ccc)
        if are_ping in (
                [True, False, True], [True, True, True], [False, False, True], [False, True, True]):
            rating = 2
        elif are_ping == [False, False, False]:
            rating = 0
        return rating

    chinese_char_combinations.extend(chinese_word)
    # print '<<<<<<', chinese_char_combinations
    full_names_to_be_rated = map(lambda w:
                                 [chinese_family_name[0] + w[0],
                                  chinese_family_name[1] + ' ' + w[1],
                                  chinese_family_name[2],
                                  w[2],
                                  w[3],
                                  (chinese_family_name[3] + w[4]) / 2,
                                  ],
                                 chinese_char_combinations)
    # print '>>>>>>', full_names_to_be_rated
    rated_names = map(lambda fnm: list(fnm) + [pingze_rating(fnm[2:5])], full_names_to_be_rated)
    rated_names = sorted(rated_names, key=lambda n: n[6], reverse=True)
    return rated_names


def _choose_family_name_by_character(order_client_chars, data):
    """

    :param order_client_chars:
    :return: {'姓', 拼音, 音调, 打分}
    """
    # TODO 姓氏缺性格分数
    rand = int(random() * len(data))
    d = data[rand]
    return d[0], d[1], int(d[2]), 5


def _mix_chinese_chars(chinese_chars):
    """
    组合单字成为二字词组
    Assume 3 chars to mix

    :param chinese_chars: [{'汉', 拼音, 音调, 打分}, ...]
    :return: [{'词组', '拼音组', 音调1, 音调2, 平均分}]
    """
    return [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)] | \
           select(lambda x: [
               (chinese_chars[x[0]][0] + chinese_chars[x[1]][0]),
               (chinese_chars[x[0]][1] + chinese_chars[x[1]][1]),
               (int(chinese_chars[x[0]][2])),
               (int(chinese_chars[x[1]][2])),
               ((chinese_chars[x[0]][3] + chinese_chars[x[1]][3]) / 2.0),
           ]) | as_list


def deliver_name(order_client_chars, order_client_gender, english_name=''):
    chinese_chars = _choose_name_by_character_and_gender(order_client_chars, order_client_gender)[
                    0:10]  # TODO itertools.count(5) | take(10) | islice(2,5) | as_list
    chinese_char_combinations = _mix_chinese_chars(chinese_chars)
    print '===========', chinese_char_combinations
    chinese_word = _find_existing_name_word(english_name, [], data=_read_csv('name_words.txt'))
    print '======', chinese_word
    chinese_family_name = _choose_family_name_by_character(order_client_chars, data=_read_csv('family_names.txt'))
    print '=========', chinese_family_name
    chinese_names = _filter_chinese_names_by_tones(chinese_family_name, chinese_char_combinations, chinese_word)
    print '==============', chinese_names
    return chinese_names


# TODO
class Chinese(object):
    def __add__(self, other):
        return other
