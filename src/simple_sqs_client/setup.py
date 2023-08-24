from setuptools import setup, find_packages

setup(
    name='simple_sqs_client',
    version='0.9.6',
    author='Aleksander Laurowski',
    author_email='aleksander.laurowski1991@gmail.com',
    description='A very simple package for interacting with SQS (Simple Queue Service) in AWS',
    packages=find_packages(),
    install_requires=['boto3'],
)
