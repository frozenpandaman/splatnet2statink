#!/usr/bin/env python

from distutils.core import setup

setup(name='splatnet2statink',
      version='0.1',
      description='script that uploads battle data from the SplatNet 2 app to stat.ink',
      author='eli fessler',
      author_email='eliwf8@gmail.com',
      url='https://github.com/frozenpandaman/splatnet2statink',
      install_requires=[
        'requests',
        'msgpack-python',
        'future',
        'pillow'
      ],
      packages=[
        'splatnet2statink'
      ],
      entry_points={
        'console_scripts': [
          'splatnet2statink = splatnet2statink.splatnet2statink:main'
        ]
      }
     )
