import unittest

from lib.challenge.user.domain.surname import Surname


class TestSurname(unittest.TestCase):
    def test_create_name_ok(self):
        surname_result = Surname.new("Woltz-Steeward")
        surname = surname_result.ok_value
        self.assertEqual(surname.value(), "Woltz-Steeward")

    def test_create_name_ko(self):
        long_surname = "long"*60
        surname_result = Surname.new(long_surname)
        surname_error = surname_result.err_value
        self.assertEqual(surname_error, f"Invalid surname length in `{long_surname}`: " +
                         "Surnames can't be longer than 150 chars")

    def test_name_eq(self):
        surname_result_1 = Surname.new("John")
        surname_1 = surname_result_1.ok_value
        surname_result_2 = Surname.new("John")
        surname_2 = surname_result_2.ok_value
        self.assertEqual(surname_1, surname_2)

    def test_name_not_eq(self):
        surname_result_1 = Surname.new("John")
        surname_1 = surname_result_1.ok_value
        surname_result_2 = Surname.new("Anna")
        surname_2 = surname_result_2.ok_value
        self.assertNotEqual(surname_1, surname_2)


if __name__ == '__main__':
    unittest.main()
