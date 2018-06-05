import os
from setuptools import setup, find_packages


path = os.path.dirname(os.path.realpath(__file__))

with open("{}/requirements.txt".format(path)) as f:
    requirements = f.read().splitlines()

entry_points = {
    'console_scripts': [
        'zapier-fun = zapier_fun.app:main'
    ]
}

setup(
    name='zapier-fun',
    description='Having some fun with Zapier',
    author='Justin Hunthrop',
    author_email='jhunthrop@gmail.com',
    packages=find_packages(),
    package_data={
        'zapier_fun.static': ['*'],
        'zapier_fun.templates': ['*']
    },
    include_package_data=True,
    version='0.0.1',
    install_requires=requirements,
    entry_points=entry_points
)
