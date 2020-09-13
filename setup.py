from setuptools import setup


def _long_description():
    with open("README.md", "r") as fh:
        return fh.read()


setup(
    name='parseval',
    packages=["parseval"],
    version="1.0.0",
    license='MIT',
    description='parseval is a data validation tool for python. It provides numerous API to parse and validate data for all native data-types. it handles data on atomic level and focuses on validation part primarily.',
    author='Saumalya Sarkar',
    author_email='saumalya75@gmail.com',
    url='https://parseval.readthedocs.io/en/latest/',
    download_url='https://github.com/saumalya75/parseval/archive/v1.0.0.tar.gz',
    keywords=['python'],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    long_description=_long_description(),
    long_description_content_type="text/markdown"
)
