from os import path
from codecs import open
from setuptools import setup, find_packages




here = path.abspath(path.dirname(__file__))
readme_path = path.join(here, 'README.md')

if path.exists(readme_path):
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = "This is my vantage6 algorithm package to check robustness."



# Here you specify the meta-data of your package. The `name` argument is
# needed in some other steps.
setup(
    name='v6-robustness-py',
    version="1.0.0",
    description='vantage6 robustness',
    long_description= long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'vantage6-algorithm-tools',
        'pandas'
    ]
)
