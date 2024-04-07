import unittest

from lib.challenge.user.domain.hobbies import Hobbies


class TestHobbies(unittest.TestCase):
    def test_create_hobbies(self):
        hobbies = Hobbies.new(" Hobby B   \n Hobby C     \n     Hobby A     ")
        expected_hobbies_values = [
            "Hobby A",
            "Hobby B",
            "Hobby C",
        ]
        self.assertEqual(hobbies.value(), expected_hobbies_values)

    def test_email_eq(self):
        hobbies_1 = Hobbies.new("Hobby 1\nHobby2\nHobby 3")
        hobbies_2 = Hobbies.new("Hobby 1\nHobby2\nHobby 3")
        self.assertEqual(hobbies_1, hobbies_2)

    def test_email_not_eq(self):
        hobbies_1 = Hobbies.new("Hobby 1\nHobby2\nHobby 3")
        hobbies_2 = Hobbies.new("Hobby 1\nHobby2")
        self.assertNotEqual(hobbies_1, hobbies_2)


if __name__ == '__main__':
    unittest.main()
