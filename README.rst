proxmove :: Proxmox VM migrator
===============================

Migrate VMs between different Proxmox VM clusters.


Config
------

Set up the ``~/.proxmoverc`` config file to look like this:

.. code-block:: ini

    [cluster1]
    ; The 'monitor' pve user needs PVEVMAdmin permissions on /. Not only
    ; to create and rename VMs, but also to enumerate the VMIDs in use.
    proxmoxapi=https://migrator@pve:secret1@cluster1.proxmox.com:443
    
    [cluster2]
    proxmoxapi=https://migrator@pve:secret2@cluster2.proxmox.com:443


Example:

.. code-block:: console

    $ ./proxmove cluster1 cluster2 machine-to-move
    Moving from cluster1<e1400248> to cluster2<6669ad2c>
    - machine-to-move
      source machine-to-move@pve08<qemu/520/running>
      listing disk 'ide2': san06:iso/debian-8.0.0-amd64-netinst.iso,media=cdrom
      listing disk 'virtio0': san08:520/vm-520-disk-1.qcow2,format=qcow2,...
      destination machine-to-move@mc9-8<qemu/123/stopped>
      stopping machine-to-move@pve08<qemu/520/running>
      stopped machine-to-move@pve08<qemu/520/stopped>
      commented machine-to-move@pve08<qemu/520/stopped>
      renamed machine-to-move--MIGRATED@pve08<qemu/520/stopped>


See the help for more options:

.. code-block:: console

    usage: proxmove [-h] [-c FILENAME] [-n] [--version]
                    source destination vm [vm ...]
    
    Migrate VMs from one Proxmox cluster to another.
    
    positional arguments:
      source                alias of source cluster
      destination           alias of destination cluster
      vm                    one or more VMs (guests) to move
    
    optional arguments:
      -h, --help            show this help message and exit
      -c FILENAME, --config FILENAME
                            use alternate configuration inifile
      -n, --dry-run         stop before doing any writes
      --version             show program's version number and exit
    
    Cluster aliases should be defined in ~/.proxmoverc (or see -c option). Define
    sections with the cluster name in brackets. The proxmoxapi= setting specifies
    how to reach the Proxmox API using common https://user:pass@host:port syntax.


License
-------

proxmove is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, version 3 or any later version.


Future
------

Future enhancements:

* Migrating the disk should be done automatically.
* Configuration translation should be more flexible.
