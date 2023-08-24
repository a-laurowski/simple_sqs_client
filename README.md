# Very Sipmle SQS Client

## Requirements
- Python 3+
## Installing
`pip install simple-sqs-client`

## Usage
### SQSClientBuilder

You can use SQSClientBuilder which is more flexible approach and allows you to fill the connection parameters in different moment of code execution if necessary.
Just keep the variable holding the builder in the scope
``` 
with SQSClientBuilder() \
            .with_region(AWS_SQS_REGION) \
            .with_queue_url(AWS_SQS_QUEUE_REACT_URL) \
            .with_aws_credentials(
        aws_access_key_id=AWS_SQS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SQS_SECRET_ACCESS_KEY
    ).build() as sqs_client:
    event = {message: "hello world"}
    sqs_client.send_message(body=json_util.dumps(event))
```

### Direct
You can also create Client using its constructor
```
  SQSClient(region_name, aws_access_key_id, aws_secret_access_key, queue_url)
```
