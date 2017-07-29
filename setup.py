import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pypluggy',
    version='0.0.9',
    description='pypluggy is a lightweight plugin framework for python',
    long_description='pypluggy is a lightweight plugin framework for python',
    url='https://veltzer.github.io/pypluggy',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='plugin python',
    packages=setuptools.find_packages(),
)
