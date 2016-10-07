proxmove :: Proxmox VM migrator
===============================

*Migrate VMs between different Proxmox VE clusters.*

Migrating a virtual machine (VM) on a PVE-cluster from one node to
another is implemented in the Proxmox Virtual Environment (PVE). But
migrating a VM from one PVE-cluster to another is not.

proxmove helps you move VMs between PVE-clusters with minimal hassle.

.. code-block:: console

    usage: proxmove [-h] [-c FILENAME] [-n] [--bwlimit MBPS] [--skip-disks]
                    [--skip-start] [--version]
                    source destination nodeid storage vm [vm ...]

    Migrate VMs from one Proxmox cluster to another.

    positional arguments:
      source                alias of source cluster
      destination           alias of destination cluster
      nodeid                node on destination cluster
      storage               storage on destination node
      vm                    one or more VMs (guests) to move

    optional arguments:
      -h, --help            show this help message and exit
      -c FILENAME, --config FILENAME
                            use alternate configuration inifile
      -n, --dry-run         stop before doing any writes
      --bwlimit MBPS        limit bandwidth in Mbit/s
      --skip-disks          do the move, but skip copying of the disks; implies
                            --skip-start
      --skip-start          do the move, but do not start the new instance
      --version             show program's version number and exit

    Cluster aliases and storage locations should be defined in ~/.proxmoverc (or
    see -c option). See the example proxmoverc.sample. It requires
    [pve:CLUSTER_ALIAS] sections for the proxmox "api" URL and
    [storage:CLUSTER_ALIAS:STORAGE_NAME] sections with "ssh", "path" and "temp"
    settings.


Example run
-----------

First you need to configure ``~/.proxmoverc``; see below.

When configured, you can do something like this:

.. code-block:: console

    $ proxmove banana-cluster the-new-cluster node2 node2-ssd the-vm-to-move
    12:12:27: Attempt moving banana-cluster<e1400248> => the-new-cluster<6669ad2c> (node 'node2'): the-vm-to-move
    12:12:27: - source VM the-vm-to-move@node1<qemu/565/running>
    12:12:27: - storage 'ide2': None,media=cdrom (host=<unknown>, guest=<unknown>)
    12:12:27: - storage 'virtio0': sharedsan:565/vm-565-disk-1.qcow2,format=qcow2,iops_rd=4000,iops_wr=500,size=50G (host=37.7GiB, guest=50.0GiB)
    12:12:27: Creating new VM 'the-vm-to-move' on 'the-new-cluster', node 'node2'
    12:12:27: - created new VM 'the-vm-to-move--CREATING' as UPID:node2:00005977:1F4D78F4:57C55C0B:qmcreate:126:user@pve:; waiting for it to show up
    12:12:34: - created new VM 'the-vm-to-move--CREATING': the-vm-to-move--CREATING@node2<qemu/126/stopped>
    12:12:34: Stopping VM the-vm-to-move@node1<qemu/565/running>
    12:12:42: - stopped VM the-vm-to-move@node1<qemu/565/stopped>
    12:12:42: Ejected (cdrom?) volume 'ide2' (none) added to the-vm-to-move--CREATING@node2<qemu/126/stopped>
    12:12:42: Begin copy of 'virtio0' (sharedsan:565/vm-565-disk-1.qcow2,format=qcow2,iops_rd=4000,iops_wr=500,size=50G) to local-ssd
    12:12:42: scp(1) copy from '/pool0/san/images/565/vm-565-disk-1.qcow2' (on sharedsan) to 'root@node2.the-new-cluster.com:/node2-ssd/temp/temp-proxmove/vm-126-virtio0'
    Warning: Permanently added 'node2.the-new-cluster.com' (ECDSA) to the list of known hosts.
    vm-565-disk-1.qcow2   100%   50GB   90.5MB/s   09:26
    Connection to san.banana-cluster.com closed.
    12:22:08: Temp data '/node2-ssd/temp/temp-proxmove/vm-126-virtio0' on local-ssd
    12:22:08: Writing data from temp '/node2-ssd/temp/temp-proxmove/vm-126-virtio0' to '/dev/zvol/node2-ssd/vm-126-virtio0' (on local-ssd)
        (100.00/100%)
    Connection to node2.the-new-cluster.com closed.
    12:24:25: Removing temp '/node2-ssd/temp/temp-proxmove/vm-126-virtio0' (on local-ssd)
    12:24:26: Starting VM the-vm-to-move@node2<qemu/126/stopped>
    12:24:27: - started VM the-vm-to-move@node2<qemu/126/running>
    12:24:27: Completed moving banana-cluster<e1400248> => the-new-cluster<6669ad2c> (node 'node2'): the-vm-to-move

Before, ``the-vm-to-move`` was running on ``banana-cluster`` on ``node1``.

Afterwards, ``the-vm-to-move`` is running on ``the-new-cluster`` on ``node2``.
The ``the-vm-to-move`` on the ``banana-cluster`` has been stopped and renamed to
``the-vm-to-move--MIGRATED``.


Configuration
-------------

Set up the ``~/.proxmoverc`` config file. First you need to define which
clusters you have. For example *banana-cluster* and *the-new-cluster*.

.. code-block:: ini

    ; Example cluster named "banana-cluster" with 3 storage devices, one
    ; shared, and two which exist on a single node only.
    [pve:banana-cluster]
    api=https://user@pve:PASSWORD@banana-cluster.com:443

    ; Example cluster named "the-new-cluster" with 2 storage devices; both
    ; storage devices exist on the respective nodes only.
    [pve:the-new-cluster]
    api=https://user@pve:PASSWORD@the-new-cluster.com:443

Next, it needs configuration for the storage devices. They are expected
to be reachable over SSH; both from the caller and from each other
(using SSH-agent forwarding).

The following defines two storage devices for the *banana-cluster*, one shared
and one local to *node1* only.

If on *sharedsan*, the images are probably called something like
``/pool0/san/images/VMID/vm-VMID-disk1.qcow2``, while in Proxmox, they are
referred to as ``sharedsan:VMID/vm-VMID-disk1.qcow2``.

.. code-block:: ini

    [storage:banana-cluster:sharedsan] ; "sharedsan" is available on all nodes
    ssh=root@san.banana-cluster.com
    path=/pool0/san/images
    temp=/pool0/san/private

    [storage:banana-cluster:local@node1] ; local disk on node1 only
    ssh=root@node1.banana-cluster.com
    path=/srv/images
    temp=/srv/temp

If you use ZFS storage on *the-new-cluster*, the storage bits could look
like this. Disk volumes exist on the ZFS pool ``node1-ssd`` and
``node2-ssd`` on the nodes *node1* and *node2* respectively.

Note that the ``temp=`` path is always a regular path.

.. code-block:: ini

    [storage:the-new-cluster:node1-ssd@node1]
    ssh=root@node1.the-new-cluster.com
    path=zfs:node1-ssd
    temp=/node1-ssd/temp

    [storage:the-new-cluster:node2-ssd@node2]
    ssh=root@node2.the-new-cluster.com
    path=zfs:node2-ssd
    temp=/node2-ssd/temp

The config file looks better with indentation. The author suggests this layout:

.. code-block:: ini

    [pve:banana-cluster]
    ...

      [storage:banana-cluster:sharedsan]
      ...
      [storage:banana-cluster:local@node1]
      ...

    [pve:the-new-cluster]
    ...

      [storage:the-new-cluster:node1-ssd@node1]
      ...


License
-------

proxmove is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, version 3 or any later version.
