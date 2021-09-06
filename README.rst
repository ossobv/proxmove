|proxmove|
==========

*The Proxmox VM migrator: migrates VMs between different Proxmox VE clusters.*

Migrating a virtual machine (VM) on a PVE-cluster from one node to
another is implemented in the Proxmox Virtual Environment (PVE). But
migrating a VM from one PVE-cluster to another is not.

proxmove helps you move VMs between PVE-clusters with minimal hassle.
*And if you use ZFS, with minimal downtime too.*


Example invocation:

.. code-block:: console

    $ proxmove SOURCE_CLUSTER DEST_CLUSTER DEST_NODE DEST_STORAGE VM_NAME1...

But, to get it to work, you'll need to configure ``~/.proxmoverc``
first. See `Configuration`_.


Additional tips:

- If source and destination filesystems use ZFS, the move is done in two
  stages, by copying an initial snapshot while the source VM is still
  up. Combine with ``--wait-before-stop`` for additional control.
- Use ``--debug``; it doesn't flood your screen, but provides useful clues
  about what it's doing.
- If your network bridge is different on the ``DEST_CLUSTER``, use
  ``--skip-start``; that way *proxmove* "completes" successfully when
  done with the move. (You'll still need to change the bridge before
  starting the VM obviously.)
- If *proxmove* detects that a move was in progress, it will
  interactively attempt a resume. For ZFS to ZFS syncs, it will do
  *another* initial resync before shutting down the source VM.


Full invocation specification (``--help``):

.. code-block::

    usage: proxmove [-c FILENAME] [-n] [--bwlimit MBPS] [--no-verify-ssl]
                    [--skip-disks] [--skip-start] [--wait-before-stop]
                    [--ssh-ciphers CIPHERS] [--debug] [--ignore-exists]
                    [-h] [--version]
                    source destination nodeid storage vm [vm ...]

    Migrate VMs from one Proxmox cluster to another.

    positional arguments:
      source                alias of source cluster
      destination           alias of destination cluster
      nodeid                node on destination cluster
      storage               storage on destination node
      vm                    one or more VMs (guests) to move

    optional arguments:
      -c FILENAME, --config FILENAME
                            use alternate configuration inifile
      -n, --dry-run         stop before doing any writes
      --bwlimit MBPS        limit bandwidth in Mbit/s
      --no-verify-ssl       skip ssl verification on the api hosts
      --skip-disks          do the move, but skip copying of the disks;
                            implies --skip-start
      --skip-start          do the move, but do not start the new instance
      --wait-before-stop    prepare the move, but ask for user
                            confirmation before shutting down the old
                            instance (useful if you have to move
                            networks/IPs)
      --ssh-ciphers CIPHERS
                            comma separated list of ssh -c ciphers to
                            prefer, (aes128-gcm@openssh.com is supposed to
                            be fast if you have aes on your cpu); set to
                            "-" to use ssh defaults

    debug arguments:
      --debug               enables extra debug logging
      --ignore-exists       continue when target VM already exists; allows
                            moving to same cluster

    other actions:
      -h, --help            show this help message and exit
      --version             show program's version number and exit

    Cluster aliases and storage locations should be defined in
    ~/.proxmoverc (or see -c option). See the example proxmoverc.sample.
    It requires [pve:CLUSTER_ALIAS] sections for the proxmox "api" URL and
    [storage:CLUSTER_ALIAS:STORAGE_NAME] sections with "ssh", "path" and
    "temp" settings.


Example run
-----------

First you need to configure ``~/.proxmoverc``; see below.

When configured, you can do something like this:

.. code-block:: console

    $ proxmove apple-cluster banana-cluster node2 node2-ssd the-vm-to-move
    12:12:27: Attempt moving apple-cluster<e1400248> => banana-cluster<6669ad2c> (node 'node2'): the-vm-to-move
    12:12:27: - source VM the-vm-to-move@node1<qemu/565/running>
    12:12:27: - storage 'ide2': None,media=cdrom (host=<unknown>, guest=<unknown>)
    12:12:27: - storage 'virtio0': sharedsan:565/vm-565-disk-1.qcow2,format=qcow2,iops_rd=4000,iops_wr=500,size=50G (host=37.7GiB, guest=50.0GiB)
    12:12:27: Creating new VM 'the-vm-to-move' on 'banana-cluster', node 'node2'
    12:12:27: - created new VM 'the-vm-to-move--CREATING' as UPID:node2:00005977:1F4D78F4:57C55C0B:qmcreate:126:user@pve:; waiting for it to show up
    12:12:34: - created new VM 'the-vm-to-move--CREATING': the-vm-to-move--CREATING@node2<qemu/126/stopped>
    12:12:34: Stopping VM the-vm-to-move@node1<qemu/565/running>
    12:12:42: - stopped VM the-vm-to-move@node1<qemu/565/stopped>
    12:12:42: Ejected (cdrom?) volume 'ide2' (none) added to the-vm-to-move--CREATING@node2<qemu/126/stopped>
    12:12:42: Begin copy of 'virtio0' (sharedsan:565/vm-565-disk-1.qcow2,format=qcow2,iops_rd=4000,iops_wr=500,size=50G) to local-ssd
    12:12:42: scp(1) copy from '/pool0/san/images/565/vm-565-disk-1.qcow2' (on sharedsan) to 'root@node2.banana-cluster.com:/node2-ssd/temp/temp-proxmove/vm-126-virtio0'
    Warning: Permanently added 'node2.banana-cluster.com' (ECDSA) to the list of known hosts.
    vm-565-disk-1.qcow2   100%   50GB   90.5MB/s   09:26
    Connection to san.apple-cluster.com closed.
    12:22:08: Temp data '/node2-ssd/temp/temp-proxmove/vm-126-virtio0' on local-ssd
    12:22:08: Writing data from temp '/node2-ssd/temp/temp-proxmove/vm-126-virtio0' to '/dev/zvol/node2-ssd/vm-126-virtio0' (on local-ssd)
        (100.00/100%)
    Connection to node2.banana-cluster.com closed.
    12:24:25: Removing temp '/node2-ssd/temp/temp-proxmove/vm-126-virtio0' (on local-ssd)
    12:24:26: Starting VM the-vm-to-move@node2<qemu/126/stopped>
    12:24:27: - started VM the-vm-to-move@node2<qemu/126/running>
    12:24:27: Completed moving apple-cluster<e1400248> => banana-cluster<6669ad2c> (node 'node2'): the-vm-to-move

Before, ``the-vm-to-move`` was running on ``apple-cluster`` on ``node1``.

Afterwards, ``the-vm-to-move`` is running on ``banana-cluster`` on ``node2``.
The ``the-vm-to-move`` on the ``apple-cluster`` has been stopped and renamed to
``the-vm-to-move--MIGRATED``.


Configuration
-------------

Set up the ``~/.proxmoverc`` config file. First you need to define which
clusters you have. For example *apple-cluster* and *banana-cluster*.

.. code-block:: ini

    ; Example cluster named "apple-cluster" with 3 storage devices, one
    ; shared, and two which exist on a single node only.
    ;
    ; The user requires various permissions found in the PVEVMAdmin role (VM
    ; allocate + audit) and PVEAuditor role (Datastore audit) and PVEPoolAdmin
    ; (to inspect and create pools).
    ;
    [pve:apple-cluster]
    api=https://user@pve:PASSWORD@apple-cluster.com:443

    ; Example cluster named "banana-cluster" with 2 storage devices; both
    ; storage devices exist on the respective nodes only.
    [pve:banana-cluster]
    api=https://user@pve:PASSWORD@banana-cluster.com:443

Next, it needs configuration for the storage devices. They are expected
to be reachable over SSH; both from the caller and from each other
(using SSH-agent forwarding).

The following defines two storage devices for the *apple-cluster*, one shared
and one local to *node1* only.

If on *sharedsan*, the images are probably called something like
``/pool0/san/images/VMID/vm-VMID-disk1.qcow2``, while in Proxmox, they are
referred to as ``sharedsan:VMID/vm-VMID-disk1.qcow2``.

.. code-block:: ini

    [storage:apple-cluster:sharedsan] ; "sharedsan" is available on all nodes
    ssh=root@san.apple-cluster.com
    path=/pool0/san/images
    temp=/pool0/san/private

    [storage:apple-cluster:local@node1] ; local disk on node1 only
    ssh=root@node1.apple-cluster.com
    path=/srv/images
    temp=/srv/temp

If you use ZFS storage on *banana-cluster*, the storage config could look
like this. Disk volumes exist on the ZFS filesystem ``node1-ssd/images``
and ``node2-ssd/images`` on the nodes *node1* and *node2* respectively.

Note that the ``temp=`` path is always a regular path.

.. code-block:: ini

    [storage:banana-cluster:node1-ssd@node1]
    ssh=root@node1.banana-cluster.com
    path=zfs:node1-ssd/images
    temp=/node1-ssd/temp

    [storage:banana-cluster:node2-ssd@node2]
    ssh=root@node2.banana-cluster.com
    path=zfs:node2-ssd/images
    temp=/node2-ssd/temp

The config file looks better with indentation. The author suggests this layout:

.. code-block:: ini

    [pve:apple-cluster]
    ...

      [storage:apple-cluster:sharedsan]
      ...
      [storage:apple-cluster:local@node1]
      ...

    [pve:banana-cluster]
    ...

      [storage:banana-cluster:node1-ssd@node1]
      ...


Debugging
---------

If you run into a ``ResourceException``, you may want to patch proxmoxer 1.0.3
to show the HTTP error reason as well.

.. code-block:: udiff

    --- proxmoxer/core.py	2019-04-04 09:13:16.832961589 +0200
    +++ proxmoxer/core.py	2019-04-04 09:15:45.434175030 +0200
    @@ -75,8 +75,10 @@ class ProxmoxResource(ProxmoxResourceBas
             logger.debug('Status code: %s, output: %s', resp.status_code, resp.content)

             if resp.status_code >= 400:
    -            raise ResourceException("{0} {1}: {2}".format(resp.status_code, httplib.responses[resp.status_code],
    -                                                          resp.content))
    +            raise ResourceException('{0} {1} ("{2}"): {3}'.format(
    +                resp.status_code, httplib.responses[resp.status_code],
    +                resp.reason,  # reason = textual status_code
    +                resp.content))
             elif 200 <= resp.status_code <= 299:
                 return self._store["serializer"].loads(resp)

It might reveal a bug (or new feature), like::

    proxmoxer.core.ResourceException:
      500 Internal Server Error ("only root can set 'vmgenid' config"):
      b'{"data":null}'


License
-------

proxmove is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, version 3 or any later version.


.. |proxmove| image:: assets/proxmove_head.png
    :alt: proxmove
