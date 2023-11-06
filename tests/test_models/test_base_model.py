#!/usr/bin/python3
''' Unittest for base_model module'''
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    ''' Test cases for the BaseModel class'''

    def test_instantiation(self):
        ''' Test for BaseModel instantiation'''
        example = BaseModel()
        self.assertIsInstance(example, BaseModel)


if __name__ == '__main__':
    unittest.main()
