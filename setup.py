#from ez_setup import use_setuptools
#use_setuptools()
from setuptools import setup, find_packages

setup(name="VLCRC",
      version="0.1dev",
      description="VLC RC interface bridge",
      author="Nick Fisher",
      packages = find_packages(),
      zip_safe = True,
      entry_points = {
          'console_scripts': [
              'vlcrc-easy = vlcrc.easy:main',
          ]
      }
     )
