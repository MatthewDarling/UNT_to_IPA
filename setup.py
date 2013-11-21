from setuptools import setup

import UNT_to_IPA

setup(
    name='UNT_to_IPA',
    version=UNT_to_IPA.__version__,
    url="https://github.com/MatthewDarling/UNT_to_IPA/"
    py_modules=['UNT_to_IPA'],
    install_requires=['re_transliterate', 'basic_argparse'],
    include_package_data=True,

    #Metadata
    description='A script to convert files to/from Upper Necaxa Totonac IPA/UNT orthography',
    long_description=(open('readme.rst').read() + '\n\n' +
                      open('CHANGELOG.rst').read()),
    license='http://opensource.org/licenses/MIT',
    author='Matthew Darling',
    author_email='matthewjdarling@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering'],
)