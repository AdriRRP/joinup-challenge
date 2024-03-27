import unittest

from lib.challenge.user.domain.user.phone import Phone


class TestPhone(unittest.TestCase):
    def test_create_phone_ok(self):
        phone_result = Phone.new("666 666 666")
        phone = phone_result.ok_value
        self.assertEqual(phone.value(), "666 666 666")

    def test_create_phone_ko(self):
        phone_result = Phone.new("invalid^phone")
        phone_error = phone_result.err_value
        self.assertEqual(phone_error, "Invalid phone format in `invalid^phone`")

    def test_phone_eq(self):
        phone_result_1 = Phone.new("666 666 666")
        phone_1 = phone_result_1.ok_value
        phone_result_2 = Phone.new("666 666 666")
        phone_2 = phone_result_2.ok_value
        self.assertEqual(phone_1, phone_2)

    def test_phone_not_eq(self):
        phone_result_1 = Phone.new("666 666 666")
        phone_1 = phone_result_1.ok_value
        phone_result_2 = Phone.new("666 666 660")
        phone_2 = phone_result_2.ok_value
        self.assertNotEqual(phone_1, phone_2)


if __name__ == '__main__':
    unittest.main()
