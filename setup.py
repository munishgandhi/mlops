import pkg_resources
from setuptools import find_packages, setup
import os

requirements = []
setup(
    name='mlops',
    version='0.0.1',
    url='https://github.com/munishgandhi/mlops',
    author='Rama Challa',
    author_email='rama@hy.ly',
    packages = find_packages(),
    # py_modules=['hyly_shims'],
    install_requires=requirements + [str(r) for r in pkg_resources.parse_requirements(open(os.path.join(os.path.dirname(__file__), "requirements.txt")))],

)