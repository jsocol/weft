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


Use
---

You have a new VM somewhere, like EC2 or Rackspace. It has whatever
standard distribution. It's on, sshd is running, and you can log in as
root, but that's it. What now?

::

    $ weft sync -H weft.example.com --initial
    root password: 
    hostname [weft]: 
    public_ip [12.34.56.78]: 
    private_ip []: 172.16.12.34
    ...
    All done! Reboot? [Yn] Y
    $

All of the variables come from writing things like ``%{HOSTNAME:host}``
in your configuration files, and weft will do its best to guess
defaults. These will only be requested with the ``--initial`` flag,
otherwise they'll be remembered remotely.


Configuration
-------------

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

    packages:
     - supervisor
     - memcached
     - gcc

    services:
     - memcached
     - supervisord

    directories:
      /opt/web:
        user: nobody
        group: web
        permissions: 0775

    files:
      /etc/ssh/sshd_config: etc/ssh/sshd_config
      /etc/sysctl.conf: etc/sysctl.conf


Concepts
========

Roles
-----

While weft is certainly helpful for synchronizing the state of a single
host, it's more useful to apply state (e.g. adding an SSH key or
installing new nginx configs) to a set of hosts.

Weft allows specifying **roles**, much like Fabric_. Roles group
together sets of hosts, but they also group together sets of state
definitions. 

When synchronizing or adding a role, weft will take the union of all the
roles that apply to a host. When removing a role, weft will take the
union of all remaining roles and remove, stop, or undo anything in the
complement.


.. _Fabric: http://fabfile.org/
.. _Puppet: http://puppetlabs.com/
.. _Chef: http://www.opscode.com/chef/
.. _Ansible: http://www.ansibleworks.com/configuration-management/
.. _Salt: http://docs.saltstack.com/topics/
