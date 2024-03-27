import unittest

from lib.shared.domain.value_object.uuid import Uuid


class TestUuid(unittest.TestCase):
    def test_create_uuid_ok(self):
        uuid_result = Uuid.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7")
        uuid = uuid_result.ok_value
        self.assertEqual(uuid.value(), "6b0fba2d-e73f-4e33-9e65-92b7621d66b7")

    def test_create_uuid_ko(self):
        uuid_result = Uuid.new("invalid^uuid")
        uuid_error = uuid_result.err_value
        self.assertEqual(uuid_error, "Invalid Uuid `invalid^uuid`: badly formed hexadecimal UUID string")

    def test_email_eq(self):
        uuid_result_1 = Uuid.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7")
        uuid_1 = uuid_result_1.ok_value
        uuid_result_2 = Uuid.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7")
        uuid_2 = uuid_result_2.ok_value
        self.assertEqual(uuid_1, uuid_2)

    def test_email_not_eq(self):
        uuid_result_1 = Uuid.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7")
        uuid_1 = uuid_result_1.ok_value
        uuid_result_2 = Uuid.new("848df41f-8d90-4bf5-a0ab-22292766e6b0")
        uuid_2 = uuid_result_2.ok_value
        self.assertNotEqual(uuid_1, uuid_2)


if __name__ == '__main__':
    unittest.main()
