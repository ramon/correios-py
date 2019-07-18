import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='correios-py',
    version='0.1.0',
    url='https://github.com/ramon/correios-py',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='short description soon',
    long_description=README,
    author='Ramon Soares',
    author_email='ramon@codecraft63.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.7, <4',
)
