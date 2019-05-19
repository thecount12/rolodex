"""
unittest for rolodex.py
"""

import unittest
from rolodex import Rolodex


class TestRolodex(unittest.TestCase):
    """
    unittest Rolodex
    """
    def setUp(self):
        """
        instantiate
        """
        self.output = Rolodex('data.csv')

    def test_input_data(self):
        """
        Test file context
        """
        self.assertIsInstance(self.output.input_data(), cls=list)

    def test_name_check(self):
        """
        Test name check and middle initial
        """
        self.assertIsInstance(self.output.name_check("peter king"), cls=tuple)
        self.assertIsInstance(self.output.name_check("peter J. king"), cls=tuple)

    def test_digits(self):
        """
        Test phone number digits color
        """
        self.assertIsInstance(self.output._digits("12345"), cls=bool)
        self.assertIsInstance(self.output._digits(" 123 123 1234"), cls=bool)
        self.assertIsInstance(self.output._digits("orange"), cls=bool)

    def test_find(self):
        """
        Test zip code, color and phone
        Also test errors and out of order
        Should return (zip, phone, color)
        """
        self.assertIsInstance(self.output.find(["12345", "blue", "831 295 0035"]), cls=tuple)
        self.assertIsInstance(self.output.find(["12345", "blue", "(831)-295-0035"]), cls=tuple)
        self.assertEqual(self.output.find(["blue", "12345", " 831 295 0035"]), ("12345", "831-295-0035", "blue"))
        self.assertEqual(self.output.find(["blue", "12345", "(831)-295-0035"]), ("12345", "831-295-0035", "blue"))

    def test_build_dict(self):
        """
        test dict creation and order, also test valid data and invalid data
        """
        self.assertIsInstance(self.output.build_dict("will", "gunn", "12345", "831-295-0035", "blue"), cls=dict)
        self.assertEqual(self.output.build_dict("will", "gunn", "12345", " 831 295 0035", "blue"),
                         {"color": "blue",
                          "firstname": "will",
                          "lastname": "gunn",
                          "zipcode": "12345",
                          "phonenumber": "831-295-0035",
                          })
        self.assertEqual(self.output.build_dict("will", "gunn", "12345", " 831 295 0035555555", "blue"),
                         {"Error": "Error"})
        self.assertEqual(self.output.build_dict("will", "gunn", "1234577777777", " 831 295 0035", "blue"),
                         {"Error": "Error"})

    def test_validate_fields(self):
        """
        test output ist
        """
        self.assertIsInstance(self.output.validate_fields(), cls=list)

    def test_format_output(self):
        """
        Returns: assert and print
        """
        self.assertIsInstance(self.output.format_output(), cls=object)


if __name__ == "__main__":
    unittest.main()
