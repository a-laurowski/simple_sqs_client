import boto3
from botocore.exceptions import WaiterError, HTTPClientError
import logging


class SQSClient:
    """
    A client for interacting with an SQS (Simple Queue Service) in AWS.
    """

    _instances = []

    def __new__(cls, *args, **kwargs) -> 'SQSClient':
        """
               Creates and returns a new instance of the SQSClient class or returns an existing instance with the same parameters.

               Args:
                   *args: Positional arguments passed during instance creation.
                   **kwargs: Keyword arguments passed during instance creation.

               Returns:
                   SQSClient: Newly created instance of the SQSClient class or an existing instance with the same parameters.

               """
        existing_instance = cls._get_existing_instance(*args, **kwargs)
        if existing_instance:
            return existing_instance
        else:
            new_instance = super().__new__(cls)
            cls._instances.append(new_instance)
            return new_instance

    def __init__(self, region_name: str, aws_access_key_id: str, aws_secret_access_key: str,
                 queue_url: str) -> 'SQSClient':
        """
        Initializes the SQS client with the specified AWS credentials and region.

        Args:
            region_name (str): The AWS region name.
            aws_access_key_id (str): The AWS access key ID.
            aws_secret_access_key (str): The AWS secret access key.
            queue_url (str): The AWS SQS queue name
        """
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.queue_url = queue_url

        self.logger = logging.getLogger(__name__)

        self._init_client()

    @classmethod
    def _get_existing_instance(
            cls, region_name: str,
            aws_access_key_id: str,
            aws_secret_access_key: str,
            queue_url: str) -> 'SQSClient':
        """
            Checks if an instance of the SQSClient class already exists with the same parameters.

            Args:
                region_name (str): AWS region name.
                aws_access_key_id (str): AWS access key ID.
                aws_secret_access_key (str): AWS secret access key.
                queue_url (str): SQS queue URL.

            Returns:
                SQSClient or None: Existing instance of SQSClient with the same parameters, or None if it doesn't exist.

            """
        for instance in cls._instances:
            if instance.region_name == region_name \
                    and instance.aws_access_key_id == aws_access_key_id \
                    and instance.aws_secret_access_key == aws_secret_access_key \
                    and instance.queue_url == queue_url:
                return instance
        return None

    def __enter__(self):
        self._init_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.sqs is not None:
            self.sqs.close()

    def _init_client(self):
        """
        Initializes the SQS client using the specified AWS credentials and region.
        """
        self.sqs = boto3.client('sqs', region_name=self.region_name,
                                aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key)

    def send_message(self, body: str) -> dict:
        """
        Sends a message to the SQS queue.

        Args:
            body (str): The body of the message as a dictionary dumped to JSON string.
        Returns:
            dict: response from AWS SQS
        Raises:
            Exception: If an error occurs while sending the message.
        """
        try:
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=body
            )
            self.logger.debug("Message sent: ID = %s", response["MessageId"])
            return response
        except Exception as e:
            self.logger.error("Failed to send message: %s", str(e))
            raise

    def read_events_with_retry(self, max_retry_attempts: int = 3, max_batch: int = 10,
                               visibility_timeout: int = 60, wait_time_seconds: int = 10) -> list:
        """
        Reads events from the SQS queue with retry.

        Args:
            wait_time_seconds (int: The amount of seconds client will be polling messages from the queue
            visibility_timeout (int): The amount of seconds,a messages stays inside the queue before getting removed
            max_retry_attempts (int): The maximum number of retry attempts.
            max_batch (int): The maximum number of messages to retrieve in each batch.

        Returns:
            list: A list of messages retrieved from the queue.

        Raises:
            HTTPClientError: If an error occurs while reading from the queue.
        """
        retry_attempt = 1

        while retry_attempt <= max_retry_attempts:
            try:
                response = self.sqs.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=max_batch,
                    MessageAttributeNames=['All'],
                    AttributeNames=['All'],
                    VisibilityTimeout=visibility_timeout,
                    WaitTimeSeconds=wait_time_seconds,
                )

                messages = response.get('Messages', [])

                return messages

            except WaiterError as e:
                self.logger.debug("WaiterError: %s", str(e))
                self.logger.debug("Retry attempt: %s", retry_attempt)
                self._init_client()
                if retry_attempt == max_retry_attempts:
                    self.logger.error("Max retry attempts reached. Exiting.")
                    raise HTTPClientError

                retry_attempt += 1

    def delete_event_from_queue(self, event: dict) -> None:
        """
        Deletes an event from the SQS queue.

        Args:
            event (dict): The event dictionary.

        Returns:
            None
        """
        self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=event['ReceiptHandle']
        )

    def purge(self) -> None:
        """
            Purges all messages from an SQS queue.
            Used for test purposes

            Returns:
                None
            """
        try:
            self.sqs.purge_queue(QueueUrl=self.queue_url)
            print("All messages have been purged from the queue.")
        except Exception as e:
            print(f"Failed to purge the queue: {str(e)}")
