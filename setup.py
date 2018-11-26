from setuptools import setup

import testrail_api

with open('readme.rst', 'r') as file:
    long_description = file.read()

setup(
    name='testrail_api',
    version=testrail_api.__version__,
    packages=['testrail_api'],
    url='https://github.com/tolstislon/testrail-api',
    license='Apache Software License 2.0',
    author='tolstislon',
    author_email='tolstislon@gmail.com',
    description='Python wrapper of the TestRail API',
    long_description=long_description,
    install_requires=['requests>=2.20.1'],
    python_requires='>=3.6',
    include_package_data=True,
    keywords=['testrail', 'api', 'client', 'library', 'testrail_api'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
