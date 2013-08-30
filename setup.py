import os
import re
from setuptools import find_packages, setup


READMEFILE = 'README.rst'
VERSIONFILE = os.path.join('victor', '__init__.py')
VSRE = r'^__version__ = ["\']([^"\']*)["\']'


def get_version():
    version_file = open(VERSIONFILE, 'rt').read()
    return re.search(VSRE, version_file, re.M).group(1)


setup(
    name='victor',
    version=get_version(),
    description='Tool to help figure out versions',
    long_description=open(READMEFILE).read(),
    license='Simplified BSD License',
    author='Will Kahn-Greene',
    author_email='willg@bluesock.org',
    url='https://github.com/willkg/victor',
    zip_safe=True,
    packages=find_packages(),
    include_package_data=True,
    scripts=['bin/victor-cmd'],
    install_requires=[
        'PyYAML',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
    ],
)
