import pkg_resources
from setuptools import find_packages, setup
import os

requirements = []

setup(
    name='hyly_chain_logger',
    version='0.0.1',
    url='https://github.com/munishgandhi/mlops/Loggers/chain_logger',
    author='Rama Challa',
    author_email='rama@hy.ly',
    py_modules=['log_chain'],
    install_requires=requirements
                     + [
                         str(r)
                         for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
                     ],

)
