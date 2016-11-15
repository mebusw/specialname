#!encoding=utf8

from django.test import TestCase
from mock import Mock
import os
from pipe import *


def read_csv(filename):
    p = os.path.join(os.path.dirname(__file__), filename)
    with open(p) as f:
        lines = f.readlines()
        lines = lines | select(lambda l: l.split(','))
    return lines | as_list


def choose_name_by_character(characters, data):
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
    print ordered
    return ordered


class TestTrainer(TestCase):
    def test_read_csv_for_male_names(self):
        data = read_csv('male_names.txt')
        self.assertEqual(150, len(data))

    def test_read_csv_for_female_names(self):
        data = read_csv('female_names.txt')
        self.assertEqual(148, len(data))

    def test_choose_name_by_character(self):
        """
            0------------3 , 4--------->
           男名,拼音,权重,音调,honorable,intellectual,elegant,agile,powerful,organized,lucky,precious,artistic,beautiful,reliable,free
        """
        data = (
            ('A', 'aaa', '', 9, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0),
            ('B', 'bbb', '', 9, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0),
            ('C', 'ccc', '', 9, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0),
        )
        user_selected_chars = (1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0)
        names = choose_name_by_character(user_selected_chars, data)
        self.assertListEqual(['A', 'B', 'C'], map(lambda n: n[0], names))

        user_selected_chars = (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1)
        names = choose_name_by_character(user_selected_chars, data)
        self.assertListEqual(['C', 'B', 'A'], map(lambda n: n[0], names))
