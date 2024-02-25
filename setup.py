from setuptools import setup, find_packages

setup(
    name='llm_strings',
    version='0.1.2',  # Update this line
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
