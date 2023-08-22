from .client import SQSClient


class SQSClientBuilder:
    """
    A builder class for creating an SQSClient with different queue and AWS credentials.
    """

    def __init__(self):
        self.region_name = None
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.queue_url = None

    def with_region(self, region_name: str) -> 'SQSClientBuilder':
        """
        Sets the AWS region name.

        Args:
            region_name (str): The AWS region name.

        Returns:
            SQSClientBuilder: The updated builder instance.
        """
        self.region_name = region_name
        return self

    def with_aws_credentials(self, aws_access_key_id: str, aws_secret_access_key: str) -> 'SQSClientBuilder':
        """
        Sets the AWS access key ID and secret access key.

        Args:
            aws_access_key_id (str): The AWS access key ID.
            aws_secret_access_key (str): The AWS secret access key.

        Returns:
            SQSClientBuilder: The updated builder instance.
        """
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        return self

    def with_queue_url(self, queue_url: str) -> 'SQSClientBuilder':
        """
        Sets the SQS queue URL.

        Args:
            queue_url (str): The SQS queue URL.

        Returns:
            SQSClientBuilder: The updated builder instance.
        """
        self.queue_url = queue_url
        return self

    def build(self) -> 'SQSClient':
        """
        Builds an instance of SQSClient with the provided configuration.

        Returns:
            SQSClient: An instance of SQSClient.
        """
        missing_fields = []

        if not self.region_name:
            missing_fields.append('region_name')
        if not self.aws_access_key_id:
            missing_fields.append('aws_access_key_id')
        if not self.aws_secret_access_key:
            missing_fields.append('aws_secret_access_key')
        if not self.queue_url:
            missing_fields.append('queue_url')

        if missing_fields:
            raise ValueError(f"Missing required SQS connection parameters: {', '.join(missing_fields)}")

        client = SQSClient(self.region_name, self.aws_access_key_id, self.aws_secret_access_key, self.queue_url)
        return client

