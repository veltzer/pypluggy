import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pyplugger',
    version='0.0.1',
    description='pyplugger is a lightweight plugin framework for python',
    long_description='pyplugger is a lightweight plugin framework for python',
    url='https://veltzer.github.io/pyplugger',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='plugin python',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
)
