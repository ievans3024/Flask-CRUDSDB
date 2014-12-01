__author__ = 'Ian S. Evans'

from setuptools import setup, find_packages

setup(
    name='Flask-CRUDSDB',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['flask', 'collection_json', 'flask_sqlalchemy'],
    url='http://github.com/ievans3024/Flask-CRUDSDB',
    license='MIT',
    author='Ian S. Evans',
    author_email='ievans3024@gmail.com',
    description='Abstraction API for creating a CRUDS interface in python for accessing databases in Flask.'
)