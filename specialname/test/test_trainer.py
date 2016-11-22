#!encoding=utf8

from django.test import TestCase
from mock import Mock
from ..views.algorithm import _read_csv, _choose_name_by_character, _find_existing_name_word, deliver_name


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


class TestAlgorithmExistingChineseWords(TestCase):
    def test_read_name_words(self):
        data = _read_csv('name_words.txt')
        self.assertEqual(195, len(data))

    def test_find_existing_name_word(self):
        data = (
            '拓理,Tony,Terry,,,0,2,0,1,2,0,0,1,0,0,0,0,,,,'.split(','),
            '卓屹,George,Gerald,,,0,1,0,0,2,0,2,1,0,0,0,0,,,,'.split(','),
            '思奋,Stephen,Stanford,,,0,2,0,0,2,0,0,0,0,0,0,0,,,,'.split(','),
        )
        english_name = 'Gerald'
        names = _find_existing_name_word(english_name, data)
        self.assertEqual('卓屹', names[0])


class TestAlgorithmDeliverCombinedNames(TestCase):
    def test_deliver_name(self):
        computed_chinese_names = deliver_name('0,0,1,1,0,0,0,0,0,1,1,1', '1')
        # self.assertEqual("", computed_chinese_names)
        # self.assertEqual(3, len(computed_chinese_names))
