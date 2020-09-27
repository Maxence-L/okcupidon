from setuptools import setup

setup(
    name='Okcupid-scrape',
    version='0.0',
    packages=['okcupid-scraper'],
    url='https://github.com/Maxence-L/Okcupid-scrape',
    license='MIT',
    author='Maxence Laumonier',
    author_email='maxence@maxence.dev',
    description='This package is designed to help you gather data automatically from users of okcupid.com.',
    install_requires=["selenium", 'bs4']
)
