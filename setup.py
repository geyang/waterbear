from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='waterbear',
      description='A utility that makes it easy to use dot notation with python dictionaries',
      long_description=long_description,
      version='1.1.2',
      url='https://github.com/episodeyang/waterbear',
      author='Ge Yang',
      author_email='yangge1987@gmail.com',
      license=None,
      keywords=['waterbear', 'dict', 'dot-notation'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3'
      ],
      packages=['waterbear'],
      install_requires=[]
      )
