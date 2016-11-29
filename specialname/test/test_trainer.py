#!encoding=utf8

from django.test import TestCase
from mock import Mock
from pipe import *
from ..views.algorithm import _read_csv, _choose_name_by_character, _find_existing_name_word, _mix_chinese_chars, \
    deliver_name, _choose_family_name_by_character


class TestAlgorithmSingleChineseChars(TestCase):
    def test_read_csv_for_male_names(self):
        data = _read_csv('male_names.txt')
        self.assertEqual(150, len(data))

    def test_read_csv_for_female_names(self):
        data = _read_csv('female_names.txt')
        self.assertEqual(148, len(data))

    def test_read_family_names(self):
        data = _read_csv('family_names.txt')
        self.assertEqual(101, len(data))

    def test_choose_name_by_character(self):
        """
            0------------3 , 4--------->
           名,拼音,权重,音调,honorable,intellectual,elegant,agile,powerful,organized,lucky,precious,artistic,beautiful,reliable,free
        """
        data = (
            ('A', 'aaa', '', 9, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0),
            ('B', 'bbb', '', 9, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0),
            ('C', 'ccc', '', 9, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0),
        )
        user_selected_chars = (1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0)
        names = _choose_name_by_character(user_selected_chars, data)
        self.assertListEqual(['A', 'B', 'C'], map(lambda n: n[0], names))

        user_selected_chars = (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1)
        names = _choose_name_by_character(user_selected_chars, data)
        self.assertListEqual(['C', 'B', 'A'], map(lambda n: n[0], names))

    def test_choose_family_name_by_character(self):
        # TODO
        user_selected_chars = (1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0)
        data = (
            ('王', 'wáng', '2', '2000'),
            ('李', 'lǐ', '3', '2000'),
            ('张', 'zhāng', '1', '2000'),
        )
        family_name = _choose_family_name_by_character(user_selected_chars, data=data)
        self.assertTrue(family_name[0] in ['王', '李', '张'])


class TestAlgorithmExistingChineseWords(TestCase):
    def test_read_name_words(self):
        data = _read_csv('name_words.txt')
        self.assertEqual(195, len(data))

    def test_find_existing_name_word(self):
        data = _read_csv('name_words.txt')
        english_name = data[0][2]
        names = _find_existing_name_word(english_name, data=data)
        self.assertEqual(data[0][0], names[0][0])

    def test_find_no_existing_name_word(self):
        english_name = 'XYZ'
        names = _find_existing_name_word(english_name, data=[])
        self.assertEqual([], names)


class TestAlgorithmDeliverCombinedNames(TestCase):
    def test_deliver_name(self):
        delivered_chinese_names = deliver_name(order_client_chars='0,0,1,1,0,0,0,0,0,1,1,1', order_client_gender='1',
                                               english_name='')
        # FIXME
        # self.assertEqual("", delivered_chinese_names)
        # self.assertEqual(3, len(delivered_chinese_names))


class TestAlgorithmMixChineseChars(TestCase):
    def test_mix(self):
        # [{'词组', '拼音组', 音调1, 音调2, 平均分}, ...]
        result = _mix_chinese_chars([('大', 'da', 4, 5), ('家', 'jia', 1, 3), ('好', 'hao', 3, 2)])

        self.assertEqual(['大家', '大好', '家大', '家好', '好大', '好家'], result | select(lambda x: x[0]) | as_list)
        self.assertEqual(['dajia', 'dahao', 'jiada', 'jiahao', 'haoda', 'haojia'],
                         result | select(lambda x: x[1]) | as_list)
        self.assertEqual([4, 4, 1, 1, 3, 3], result | select(lambda x: x[2]) | as_list)
        self.assertEqual([1, 3, 4, 3, 4, 1], result | select(lambda x: x[3]) | as_list)
        self.assertEqual([4, 3.5, 4, 2.5, 3.5, 2.5], result | select(lambda x: x[4]) | as_list)
