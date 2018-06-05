import os
from setuptools import setup, find_packages


path = os.path.dirname(os.path.realpath(__file__))

with open("{}/requirements.txt".format(path)) as f:
    requirements = f.read().splitlines()

setup(
    name='zapier-fun',
    description='Having some fun with Zapier',
    author='Justin Hunthrop',
    author_email='jhunthrop@gmail.com',
    packages=find_packages(),
    package_data={
        'zapier_fun.config': ['*.yaml'],
        'zapier_fun.ui': ['*.html']
    },
    version='0.0.1',
    install_requires=requirements
)
