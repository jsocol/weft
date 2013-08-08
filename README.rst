====
weft
====

**weft** is a configuration manager for provisioning remote systems. It
is powered by Fabric_ and is designed based on four primary guiding
principles:

1. Server configuration is state.
2. State should be recorded declaratively.
3. Remote servers should require nothing more than a running ``sshd``.
4. Changes must be pushed to remote servers.

Portability of configuration between remote operating systems is a
secondary objective.


Why not...?
===========

Why not use Puppet_, or Chef_, or Ansible_, or Salt_? Why reinvent this
particular wheel?

Puppet, Chef, and Salt all run in client-server configurations, which
violates principle 3 and means you have to bootstrap your bootstrap
process.

Ansible is close, but thinks in very imperative terms of tasks and
handlers instead of simply state.

If there are other good options out there I've missed, please let me
know!


Example
=======

::

    hosts:
      web01: 172.21.3.4
      web02: 172.21.3.5
      db01: 172.21.4.2

    groups:
     - web
    users:
      james:
        authorized_keys:
          - ssh-rsa AAAA....
          - ssh-rsa AAAAAAA.....
        group: web
    sudoers:
     - james

    services:
     - memcached
     - supervisord

    files:
      /etc/ssh/sshd_config: ssh/sshd_config
      /



.. _Fabric: http://fabfile.org/
.. _Puppet: http://puppetlabs.com/
.. _Chef: http://www.opscode.com/chef/
.. _Ansible: http://www.ansibleworks.com/configuration-management/
.. _Salt: http://docs.saltstack.com/topics/
