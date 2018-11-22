#!/usr/bin/env python3
from distutils.core import setup

with open('proxmove') as fp:
    for line in fp:
        if line.startswith('__version__'):
            version = line.split("'")[1]
            break

long_description = []
for filename in ('README.rst', 'CHANGES.rst', 'TODO.rst'):
    with open(filename) as fp:
        long_description.append(fp.read())
long_description = '\n\n'.join(long_description)


setup(
    name='proxmove',
    version=version,
    scripts=['proxmove'],
    data_files=[
        ('share/doc/proxmove', [
            'README.rst', 'CHANGES.rst', 'TODO.rst']),
        ('share/proxmove', [
            'proxmoverc.sample'])],
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
