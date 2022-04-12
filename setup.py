#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [ 'python_magnetgeo', 'sqlmodel', 'flask', 'flask-wtf' ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Christophe Trophime",
    author_email='christophe.trophime@lncmi.cnrs.fr',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Magnet DB",
    entry_points={
        'console_scripts': [
            'python_magnetdb=python_magnetdb.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='python_magnetdb',
    name='python_magnetdb',
    packages=find_packages(include=['python_magnetdb', 'python_magnetdb.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Trophime/python_magnetdb',
    version='0.1.0',
    zip_safe=False,
)
