from setuptools import setup, find_packages

setup(
  name='fcclipper',
  version='0.0.1',
  packages=find_packages(),
  license='MIT',
  author='Jeff Dunn',
  install_requires=['click','pyppeteer','rich'],
  description='Clip digital coupons and retrieve Fuel Bucks at Food City grocery stores',
  entry_points=dict(
    console_script=['fcclip=src.main:cli']
  )
)
