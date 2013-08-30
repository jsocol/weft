import os
from cStringIO import StringIO
from weft import exceptions
from weft._fab import sudo, put
from weft.providers.base.users import BaseUserProvider


AUTHORIZED_KEYS_TEMPLATE = """#
# This file is managed by weft. You can edit it,
# but it is not recommended.
%s"""


sudolist = lambda l: sudo(' '.join(l))


class UserProvider(BaseUserProvider):
    @classmethod
    def add(cls, username, group, groups, authorized_keys, password, homedir,
            nohome, shell):
        cmd = ['useradd']
        if group is not None:
            # TODO throw ConsistencyError if group does not exist.
            cmd += ['-g', group]
        if groups:
            cmd += ['-G', ','.join(groups)]
        if homedir:
            cmd += ['-d', homedir]
        if nohome:
            cmd += ['--no-create-home']
        if password:
            cmd += ['-p', password]
        if shell:
            cmd += ['-s', shell]
        cmd += [username]
        result = sudolist(cmd)
        if not result.succeeded:
            raise Exception(result.stdout)

        if authorized_keys:
            cls.set_authorized_keys(username, group, authorized_keys)
        return True

    @classmethod
    def _find_home_dir(cls, username):
        cmd = ['awk', '-F:', '-v', 'v="%s"' % username,
               "'{ if ($1 == v) print $6 }'", '/etc/passwd']
        result = sudolist(cmd)
        return result.stdout.strip()

    @classmethod
    def set_authorized_keys(cls, username, group, keys):
        path = cls._find_home_dir(username)
        sshpath = os.path.join(path, '.ssh')
        sudolist(['mkdir', '-p', sshpath])

        tmp = StringIO(AUTHORIZED_KEYS_TEMPLATE % '\n'.join(keys))
        filepath = os.path.join(sshpath, 'authorized_keys')
        put(tmp, filepath, use_sudo=True)

        usergrp = ':'.join((username, group or username))
        sudolist(['chown', '-R', usergrp, sshpath])
        sudolist(['chmod', '-R', '0700', sshpath])
        sudolist(['chmod', '0600', filepath])
        return True

    @classmethod
    def exists(cls, username):
        return sudo('id %s' % username).succeeded

    @classmethod
    def remove(cls, username, remove_homedir=True):
        cmd = ['userdel']
        if remove_homedir:
            cmd += ['-f', '-r']
        cmd += [username]
        return sudolist(cmd).succeeded
