import unittest

from lib.challenge.user.domain.user.id import Id


class TestId(unittest.TestCase):
    def test_create_id_ok(self):
        id_result = Id.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7")
        id = id_result.ok_value
        self.assertEqual(id.value(), "6b0fba2d-e73f-4e33-9e65-92b7621d66b7")

    def test_create_id_ko(self):
        id_result = Id.new("invalid^id")
        id_error = id_result.err_value
        self.assertEqual(id_error, "Invalid Id `invalid^id`: Invalid Uuid `invalid^id`: badly formed " +
                         "hexadecimal UUID string")

    def test_id_eq(self):
        id_result_1 = Id.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7")
        id_1 = id_result_1.ok_value
        id_result_2 = Id.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7")
        id_2 = id_result_2.ok_value
        self.assertEqual(id_1, id_2)

    def test_id_not_eq(self):
        id_result_1 = Id.new("6b0fba2d-e73f-4e33-9e65-92b7621d66b7")
        id_1 = id_result_1.ok_value
        id_result_2 = Id.new("848df41f-8d90-4bf5-a0ab-22292766e6b0")
        id_2 = id_result_2.ok_value
        self.assertNotEqual(id_1, id_2)


if __name__ == '__main__':
    unittest.main()
