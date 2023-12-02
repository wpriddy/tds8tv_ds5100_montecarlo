from setuptools import setup

setup(name='montecarlo',
      version='1.0',
      description='Python Distribution Utilities',
      author='Wyatt Priddy',
      url='https://github.com/wpriddy/tds8tv_ds5100_montecarlo',
      author_email='wpriddy@tds8tv.edu',
      license='MIT',
      packages=['montecarlo'],
      # Only non-standard libraries
      install_requires=['numpy>=1.19.2', 
                         'pandas>=1.1.3',
                         'matplotlib>=3.8.2']
     )