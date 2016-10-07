Changes
-------

* **v0.0.7** - 2016-10-07

  Bugs fixed:

  - Instead of trusting on the "size=XXG" which may or may not be
    present in the storage volume config, it reads the QCOW header or
    ZFS volume size directly. Also checks that the values are available
    before attempting a move.

* **v0.0.6** - 2016-09-21

  New features:

  - Add --bwlimit in Mbit/s to limit bandwidth during transfer. Will use
    the scp(1) -l option or for ZFS use the mbuffer(1) auxiliary. As an
    added bonus mbuffer may improve ZFS send/recv speed through
    buffering. Closes #4.
  - Add --skip-disks option to skip copying of the disks. Use this if
    you want to copy the disks manually. Closes #3.
  - Add --skip-start option to skip autostarting of the VM.
  - Adds optional pv(1) pipe viewer progress bar to get ETA in ZFS
    transfers.
  - Add hidden --debug option for more verbosity.
  - Add hidden --ignore-exists option that allows you to test moves
    between the same cluster by creating an alias (second config).

  Bugs fixed:

  - Format is not always specified in the properties. If it isn't, use
    the image filename suffix when available.
  - Sometimes old values aren't available in the "pending" list. Don't croak.
    Closes #2.
  - Begun refactoring. Testing bettercodehub.com.
  - Also check whether temporary (renamed) VMs exist before starting.

* **v0.0.5** - 2016-08-30

  - Added support for ZFS to ZFS disk copy. QCOW2 to ZFS and ZFS to ZFS
    is now tested.

* **v0.0.4** - 2016-08-30

  - Major overhaul of configuration format and other changes.
