from setuptools import find_packages, setup


setup(
    name='scanerr',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'requests',
        'rich',
        'typer',
    ],
    entry_points={
        'console_scripts': [
            'scanerr=src.scanerr.root:root'
        ]
    }
)
