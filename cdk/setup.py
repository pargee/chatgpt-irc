from setuptools import setup, find_packages

setup(
    name='chatgpt-irc-cdk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'aws-cdk.core',
        'aws-cdk.aws_ec2'
    ],
)
