Changes
-------

* **vHEAD** - XXXX-XX-XX

  New features:

  - Add --bwlimit in Mbit/s to limit bandwidth during transfer. Will use the
    scp(1) -l option or for ZFS use the mbuffer(1) auxiliary. As an added bonus
    mbuffer may improve ZFS send/recv speed through buffering. Closes #4.

  Bugs fixed:

  - Format is not always specified in the properties. If it isn't, use
    the image filename suffix when available.
  - Sometimes old values aren't available in the "pending" list. Don't croak.
    Closes #2.

* **v0.0.5** - 2016-08-30

  - Added support for ZFS to ZFS disk copy. QCOW2 to ZFS and ZFS to ZFS
    is now tested.

* **v0.0.4** - 2016-08-30

  - Major overhaul of configuration format and other changes.
