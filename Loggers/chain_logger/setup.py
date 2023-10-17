from setuptools import setup

setup(
    name='hyly_chain_logger',
    version='0.0.1',
    url='https://github.com/munishgandhi/mlops/Loggers/chain_logger',
    author='Rama Challa',
    author_email='rama@hy.ly',
    py_modules=['log_chain'],
    install_requires=['celery','redis','python-dotenv'],

)
