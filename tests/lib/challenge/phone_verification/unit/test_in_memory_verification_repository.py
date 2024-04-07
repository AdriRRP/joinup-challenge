import unittest

from lib.challenge.email_verification.domain.verification import Verification
from lib.challenge.email_verification.infrastructure.repository.in_memory import InMemory
from lib.challenge.user.domain.email import Email
from lib.challenge.user.domain.id import Id
from lib.shared.domain.value_object.uuid import Uuid


class TestInMemoryVerificationRepository(unittest.TestCase):
    test_verification_1 = Verification.new(
        Uuid.new("a8f4f4f8-25e1-4a61-91d4-ec8975a2e580").ok_value,
        Id.new("6287aa63-ac02-4957-8424-efb5af11cb4a").ok_value,
        Email.new("first.user@mail.com").ok_value,
    )

    test_verification_2 = Verification.new(
        Uuid.new("8a39d23f-18ba-4a02-af27-04cdd2fc2cd4").ok_value,
        Id.new("1a42a739-0ace-42ce-bbcb-04024d0fc671").ok_value,
        Email.new("second.user@mail.com").ok_value,
    )

    test_verification_3 = Verification.new(
        Uuid.new("4b1efe29-a5f0-4c65-80df-27b01e46e277").ok_value,
        Id.new("ae9028fc-4117-432a-b493-2f8eaa40689a").ok_value,
        Email.new("third.user@mail.com").ok_value,
    )

    test_verifications = [test_verification_1, test_verification_2]

    def test_in_memory_user_repository_found_by_code(self):
        repository = InMemory.new(TestInMemoryVerificationRepository.test_verifications)
        code = Uuid.new("a8f4f4f8-25e1-4a61-91d4-ec8975a2e580").ok_value
        verification_found = repository.find(code).ok_value
        self.assertEqual(verification_found, TestInMemoryVerificationRepository.test_verification_1)

    def test_in_memory_user_repository_not_found_by_id(self):
        repository = InMemory.new(TestInMemoryVerificationRepository.test_verifications)
        code = Uuid.new("00000000-0000-0000-0000-000000000000").ok_value
        verification_found = repository.find(code).ok_value
        self.assertEqual(verification_found, None)

    def test_in_memory_user_repository_save(self):
        repository = InMemory.new(TestInMemoryVerificationRepository.test_verifications)
        code = Uuid.new("4b1efe29-a5f0-4c65-80df-27b01e46e277").ok_value
        verification_found = repository.find(code).ok_value
        self.assertEqual(verification_found, None)

        repository.save(TestInMemoryVerificationRepository.test_verification_3)
        verification_found = repository.find(code).ok_value
        self.assertEqual(verification_found, TestInMemoryVerificationRepository.test_verification_3)

    def test_in_memory_verification_repository_accept(self):
        repository = InMemory.new(TestInMemoryVerificationRepository.test_verifications)
        code = Uuid.new("a8f4f4f8-25e1-4a61-91d4-ec8975a2e580").ok_value
        verification_found = repository.find(code).ok_value
        self.assertFalse(verification_found.accepted())

        repository.accept(code)
        verification_found = repository.find(code).ok_value
        self.assertTrue(verification_found.accepted())


if __name__ == '__main__':
    unittest.main()
