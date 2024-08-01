from setuptools import find_packages, setup

setup(
    name='pyver',
    packages=find_packages(),
    version='0.2.1',
    description='Python Advanced HTTP Server',
    author='Abd Rahman Alkaff',
    license='MIT',
    install_requires=[],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==4.4.1'],
    # test_suite='tests',
)

## BUILD: 
# python setup.py bdist_wheel