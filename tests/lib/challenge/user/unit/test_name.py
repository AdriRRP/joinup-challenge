import unittest

from lib.challenge.user.domain.name import Name


class TestName(unittest.TestCase):
    def test_create_name_ok(self):
        name_result = Name.new("John")
        name = name_result.ok_value
        self.assertEqual(name.value(), "John")

    def test_create_name_ko(self):
        long_name = "long"*20
        name_result = Name.new(long_name)
        name_error = name_result.err_value
        self.assertEqual(name_error, f"Invalid name length in `{long_name}`: " +
                         "Names can't be longer than 50 chars")

    def test_name_eq(self):
        name_result_1 = Name.new("John")
        name_1 = name_result_1.ok_value
        name_result_2 = Name.new("John")
        name_2 = name_result_2.ok_value
        self.assertEqual(name_1, name_2)

    def test_name_not_eq(self):
        name_result_1 = Name.new("John")
        name_1 = name_result_1.ok_value
        name_result_2 = Name.new("Anna")
        name_2 = name_result_2.ok_value
        self.assertNotEqual(name_1, name_2)


if __name__ == '__main__':
    unittest.main()
