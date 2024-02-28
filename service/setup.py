from setuptools import find_packages, setup


setup(
    name='scanerr',
    version='0.0.2',
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
