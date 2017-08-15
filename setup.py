import versioneer
from setuptools import setup, find_packages

setup(name='guidebook',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      license='GNU',
      author='Teddy Rendahl',
      packages=find_packages(),
      )
