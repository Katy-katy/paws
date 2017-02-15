"""
paws setup module
---- ----- ------
See https://packaging.python.org/distributing/
"""

#from setuptools import setup, find_packages
# To use a consistent encoding
#from codecs import open

from os import path
import setuptools

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here,'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get the code version from the version.py file, store as __version__
with open(path.join(here,'version.py') as f: 
    exec(f.read())

setup(
    name='paws',

    # Versions should comply with PEP440.  
    version=__version__,

    description='the Platform for Automated Workflows by SSRL',
    long_description=long_description,

    url='https://github.com/slaclab/paws/',
    author='Lenson A. Pellouchoud, Amanda Fournier, Fang Ren, Yuriy Kolotovsky, Ronald Pandolfi, Apurva Mehta, Christopher Tassone',
    author_email='paws-developers@slac.stanford.edu',
    license='BSD-like',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Stable',

        'Intended Audience :: Researchers, Developers',
        'Topic :: Data Analysis',

        # Pick your license as you wish (should match "license" above)
        'License :: BSD-like',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    keywords='modular data analysis workflow',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['peppercorn'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'sample': ['package_data.dat'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)