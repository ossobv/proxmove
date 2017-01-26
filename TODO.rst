TODO
----

* On missing disk (bad config), the zfs send stalls and mbuffer waits for
  infinity.

* Rename "VM" to "Instance" so "LXC" containers don't feel misrepresented.

* Communicate with the storage API to check/configure storage (more easily).

* Create a ``--config`` command to set up a basic configuration. Combine with
  storage API reading.

* Fix so LXC-copying works (this is a bit tricky because of the necessity for
  a temporary image/tarball to install).

* Create a proxmoxer_api example that returns test data, so we can run tests.

* Let it work with pve-zsync -- a daemon that syncs data between nodes:
  https://pve.proxmox.com/wiki/PVE-zsync
