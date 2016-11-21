from setuptools import setup, find_packages

install_requires = [
        "Scrapy>=0.24.4",
        "Flask>=0.10.1",
        "Twisted>=15.4.0",
        "six>=1.10.0"
]

setup(
    name='Arachne',
    version='0.5.0',
    author='Kiran Koduru',
    author_email='kiranrkoduru@gmail.com',
    packages=find_packages(),
    test_suite='arachne.tests',
    url='https://github.com/kirankoduru/arachne',
    license='BSD',
    description='API for Scrapy spiders',
    long_description=open('README.rst').read(),
    install_requires=install_requires,
)
