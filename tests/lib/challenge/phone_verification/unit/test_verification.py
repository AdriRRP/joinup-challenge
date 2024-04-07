import unittest

from lib.challenge.email_verification.domain.domain_event.created import Created
from lib.challenge.email_verification.domain.verification import Verification
from lib.challenge.user.domain.id import Id
from lib.challenge.user.domain.email import Email
from lib.shared.domain.value_object.uuid import Uuid


class VerificationTest(unittest.TestCase):
    def test_create_user(self):
        code = Uuid.new("a8f4f4f8-25e1-4a61-91d4-ec8975a2e580").ok_value
        user_id = Id.new("6287aa63-ac02-4957-8424-efb5af11cb4a").ok_value
        email = Email.new("john.doe@mail.com").ok_value

        verification = Verification.new(code, user_id, email)

        self.assertEqual(verification.code(), "a8f4f4f8-25e1-4a61-91d4-ec8975a2e580")
        self.assertEqual(verification.user_id(), "6287aa63-ac02-4957-8424-efb5af11cb4a")
        self.assertEqual(verification.email(), "john.doe@mail.com")

        events = verification.pull_domain_events()

        self.assertEqual(len(events), 1)

        event = events[0]

        self.assertTrue(isinstance(event, Created))

        event_primitives = event.to_primitive()
        expected_event_primitives = {
            'user_id': "6287aa63-ac02-4957-8424-efb5af11cb4a",
            'email': "john.doe@mail.com",
        }

        self.assertEqual(event_primitives, expected_event_primitives)

        events_again = verification.pull_domain_events()

        self.assertEqual(len(events_again), 0)


if __name__ == '__main__':
    unittest.main()
