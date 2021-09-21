from setuptools import setup, find_packages
from harp_helper import constants

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().split("\n")

setup(
    name=constants.APP_NAME,
    version=constants.VERSION,
    packages=find_packages(include=['harp_helper', 'harp_helper.*']),
    python_requires='>=3.5',
    url='',
    license='',
    author='Tim Martin',
    author_email='tim.martin.nowhere.test',
    description='Graphical Python script for Harmonica',
    install_requires=requirements,
    entry_points={
        'console_scripts': ['harp=harp_helper.main:main']
    }
)
