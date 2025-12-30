"""Setup file."""

from pathlib import Path

from setuptools import find_packages, setup

readme = Path(".", "README.md").absolute()
with readme.open("r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="testrail_api",
    packages=find_packages(exclude=("tests", "dev_tools")),
    url="https://github.com/tolstislon/testrail-api",
    license="MIT License",
    author="tolstislon",
    author_email="tolstislon@gmail.com",
    description="Python wrapper of the TestRail API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    use_scm_version={"write_to": "testrail_api/__version__.py"},
    setup_requires=["setuptools_scm"],
    install_requires=["requests>=2.32.4"],
    python_requires=">=3.9",
    include_package_data=True,
    keywords=[
        "testrail",
        "api",
        "client",
        "api-client",
        "library",
        "testrail_api",
        "testrail-api",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
