from setuptools import setup

setup(
    name='hyly_dialog_logger',
    version='0.0.1',
    url='https://github.com/munishgandhi/mlops/Loggers/usage_logger',
    author='Rama Challa',
    author_email='rama@hy.ly',
    py_modules=['log_chain'],
    install_requires=['celery','redis','python-dotenv'],

)
