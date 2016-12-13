from __future__ import unicode_literals
from setuptools import setup

exec(open('chargen/_version.py').read())
if __name__ == '__main__':
    setup(
        name='chargen',
        packages=['chargen'],
        version=__version__,
        author='Eli Courtwright',
        author_email='eli@courtwright.org',
        description='L7R Character Generation',
        url='https://github.com/EliAndrewC/chargen',
        install_requires=open('requirements.txt').readlines()
    )
