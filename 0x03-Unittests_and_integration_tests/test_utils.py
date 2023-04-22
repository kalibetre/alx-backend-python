#!/usr/bin/env python3
"""A test module for utils module
"""
import unittest

from parameterized import parameterized

access_nested_map = __import__('utils').access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """A test class for access_nested_map function
    """

    @parameterized.expand([
        (
            {
                "a": 1
            },
            ("a", ),
            1,
        ),
        (
            {
                "a": {
                    "b": 2
                }
            },
            ("a", ),
            {
                "b": 2
            },
        ),
        (
            {
                "a": {
                    "b": 2
                }
            },
            ("a", "b"),
            2,
        ),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Tests access_nested_map function with different inputs
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
