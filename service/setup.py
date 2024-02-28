from setuptools import find_packages, setup


setup(
    name='scanerr-cli',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'certifi',
        'charset-normalizer',
        'colorama',
        'idna',
        'markdown-it-py',
        'mdurl',
        'Pygments',
        'python-dotenv',
        'requests',
        'rich',
        'shellingham',
        'typer',
        'typing_extensions',
        'urllib3'
    ],
    entry_points={
        'console_scripts': [
            'scanerr=src.scanerr.root:root'
        ]
    }
)
