import re
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


def desc():
    return read('README.rst')


file_text = read(fpath('staticmaps_signature/__init__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    name='staticmaps-signature',
    version=grep('__version__'),
    url='https://github.com/allrod5/staticmaps-signature/',
    license='MIT',
    author=grep('__author__'),
    author_email=grep('__email__'),
    description='Easily sign Google StaticMap API request urls with your API Key or Client ID',
    long_description=desc(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'coverage',
        'coveralls',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
    ],
)
