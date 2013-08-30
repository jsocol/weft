class BaseUserProvider(object):
    @classmethod
    def add(cls, username, group, groups, authorized_keys, password, homedir,
            nohome, shell):
        raise NotImplementedError

    @classmethod
    def exists(cls, username):
        raise NotImplementedError

    @classmethod
    def remove(cls, username):
        raise NotImplementedError

    @classmethod
    def sync(cls, username, group, groups, authorized_keys, password, homedir,
             nohome, shell):
        raise NotImplementedError


class BaseGroupProvider(object):
    @classmethod
    def add(cls, group):
        raise NotImplementedError

    @classmethod
    def remove(cls, group):
        raise NotImplementedError
