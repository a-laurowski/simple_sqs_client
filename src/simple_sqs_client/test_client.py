import unittest
import json
import os
from botocore.exceptions import WaiterError
from .client import SQSClient


class TestSQSClientIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.region_name = os.environ.get("AWS_SQS_QUEUE_REGION")
        cls.aws_access_key_id = os.environ.get("AWS_SQS_QUEUE_ACCESS_KEY_ID")
        cls.aws_secret_access_key = os.environ.get("AWS_SQS_QUEUE_SECRET_ACCESS_KEY")
        cls.queue_url = os.environ.get("AWS_SQS_QUEUE_TEST_URL")

        cls.client = SQSClient(cls.region_name, cls.aws_access_key_id, cls.aws_secret_access_key, cls.queue_url)

    def setUp(self) -> None:
        self.client.purge()

    def tearDown(self) -> None:
        self.client.purge()

    def test_send_and_read_message(self):
        # arrange
        event_type = "LPViewEvent"
        component = "web_layer"
        body = {
            "message": "test_message",
            "cls": "LPViewEvent",
            "p": {
                "account_id": "601eeee58ff0e51d829455cc",
                "c": 12423232,
                "pid": 635424536546,
            },
        }

        try:
            # act
            self.client.send_message(body, event_type, component)
            messages = self.client.read_events_with_retry(max_retry_attempts=3, max_batch=10)

            # assert
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0]['Body'], json.dumps(body))
            self.assertEqual(messages[0]['MessageAttributes']['event_type']['StringValue'], event_type)
            self.assertEqual(messages[0]['MessageAttributes']['component']['StringValue'],
                             component)  # Check the component attribute

        except WaiterError as e:
            self.fail("Error reading message from the queue: {}".format(str(e)))
