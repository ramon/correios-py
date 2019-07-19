import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='correios-py',
    version='0.1.1',
    author='Ramon Soares',
    author_email='ramon@codecraft63.com',
    description="Correios Freigth Calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ramon/correios-py',
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.7, <4',
)
