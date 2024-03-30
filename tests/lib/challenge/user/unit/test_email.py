import unittest

from lib.challenge.user.domain.email import Email


class TestEmail(unittest.TestCase):
    def test_create_email_ok(self):
        email_result = Email.new("user@domain.ext")
        email = email_result.ok_value
        self.assertEqual(email.value(), "user@domain.ext")

    def test_create_email_ko(self):
        email_result = Email.new("invalid^email")
        email_error = email_result.err_value
        self.assertEqual(email_error, "Invalid email format in `invalid^email`")

    def test_email_eq(self):
        email_result_1 = Email.new("user@domain.ext")
        email_1 = email_result_1.ok_value
        email_result_2 = Email.new("user@domain.ext")
        email_2 = email_result_2.ok_value
        self.assertEqual(email_1, email_2)

    def test_email_not_eq(self):
        email_result_1 = Email.new("user@domain.ext")
        email_1 = email_result_1.ok_value
        email_result_2 = Email.new("other_user@domain.ext")
        email_2 = email_result_2.ok_value
        self.assertNotEqual(email_1, email_2)


if __name__ == '__main__':
    unittest.main()
