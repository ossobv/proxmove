#!/usr/bin/env python3
from distutils.core import setup

with open('proxmove') as fp:
    for line in fp:
        if line.startswith('__version__'):
            version = line.split("'")[1]
            break
with open('README.rst') as fp:
    long_description = fp.read()
with open('CHANGES.rst') as fp:
    long_description += '\n\n' + fp.read()


setup(
    name='proxmove',
    version=version,
    scripts=['proxmove'],
    data_files=[('', ['README.rst', 'CHANGES.rst', 'proxmoverc.sample'])],
    description=(
        'Migrate virtual machines between different Proxmox VM clusters'),
    long_description=long_description,
    author='Walter Doekes, OSSO B.V.',
    author_email='wjdoekes+proxmove@osso.nl',
    url='https://github.com/ossobv/proxmove',
    license='GPLv3+',
    platforms=['linux'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        ('License :: OSI Approved :: GNU General Public License v3 '
         'or later (GPLv3+)'),
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Clustering',
    ],
    install_requires=[
        'proxmoxer>=0.2.4',
        'requests>=2.9.1',
    ],
)

# vim: set ts=8 sw=4 sts=4 et ai tw=79:
