from setuptools import setup

setup(
    name='okcupidon',
    version='0.0',
    packages=['okcupidon'],
    url='https://github.com/Maxence-L/okcupidon',
    license='MIT',
    author='Maxence Laumonier',
    author_email='maxence@maxence.dev',
    description='This package is designed to help you gather data automatically from users of okcupid.com.',
    install_requires=["selenium", 'bs4', 'webdriver_manager']
)
