from setuptools import setup

setup(name='picturemap',
      version='0.0.1',
      description='Visualise pictures in a map',
      url='http://github.com/',
      author='David Valente',
      author_email='davmval@icloud.com',
      license='MIT',
      packages=['picturemap'],
      install_requires = ['exifread', 'tqdm'],
      scripts=['bin/picturemap'],
      include_package_data=True,
      zip_safe=False)
