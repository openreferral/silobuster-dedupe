from setuptools import setup, find_packages

setup(
    name='silobuster_test',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'psycopg2',
        'tld'

    ]
    # author='Your Name',
    # author_email='your.email@example.com',
    # description='A brief description of your package',
    # license='MIT',
    # keywords='keyword1 keyword2',
    # url='http://url-to-your-package-if-any'
)