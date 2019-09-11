from m2r import parse_from_file
from setuptools import setup

import testrail_api

setup(
    name='testrail_api',
    version=testrail_api.__version__,
    packages=['testrail_api'],
    url=testrail_api.__url__,
    license=testrail_api.__license__,
    author=testrail_api.__author__,
    author_email=testrail_api.__author_email__,
    description=testrail_api.__description__,
    long_description=parse_from_file('README.md'),
    install_requires=[
        'requests>=2.20.1'
    ],
    python_requires='>=3.6',
    include_package_data=True,
    keywords=[
        'testrail',
        'api',
        'client',
        'library',
        'testrail_api',
        'testrail-api'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
