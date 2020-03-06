#!/usr/bin/env python
import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8'),
    ) as fh:
        return fh.read()


# TODO: put some data into src/paxter/metadata.json
setup(
    name='paxter',
    version='0.1.0',
    license='Apache-2.0',
    description='Document-first text pre-processing mini-language '
                'loosely inspired by at-expressions in Racket',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Abhabongse Janthong',
    author_email='6845502+abhabongse@users.noreply.github.com',
    url='https://github.com/abhabongse/paxter',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # Complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Text Processing',
        'Typing :: Typed',
    ],
    project_urls={
        'Documentation': 'https://paxter.readthedocs.io/',
        'Changelog': 'https://github.com/abhabongse/paxter/blob/master/CHANGELOG.md',
        'Issue Tracker': 'https://github.com/abhabongse/paxter/issues',
    },
    keywords=[],
    python_requires='>=3.7',
    install_requires=[
        'click>=7.0',
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            '1 = paxter.commands:program',
        ],
    },
)