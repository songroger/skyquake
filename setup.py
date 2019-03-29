import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fh:
    readme = fh.read()

setup(
    name='skyquake',
    version=__import__('skyquake').__version__,
    description='skyquake',
    long_description=readme,
    packages=find_packages(),
    install_requires=[
        "requests>=2.11.1"
    ],

    # extras_require=extras_require,
    package_data={
        'skyquake': [
        ],
    },
)
