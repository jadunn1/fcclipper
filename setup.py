from setuptools import setup, find_packages

setup(
  name='fcclipper',
  version='0.0.2',
  license='MIT',
  author='Jeff Dunn',
  url='https://github.com/jadunn1/fcclipper',
  packages=find_packages(),
  install_requires=['click','pyppeteer','rich'],
  description='Clip digital coupons and retrieve Fuel Bucks at Food City grocery stores',
  entry_points={
    'console_scripts': [
      'fcclipper = fcclipper.__main__:cli',
        ],
    }
)
