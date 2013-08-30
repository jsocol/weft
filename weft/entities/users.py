from weft.providers.default.users import UserProvider, GroupProvider


class User(object):
    root_key = 'users'
    uses_key = True
    default_provider = UserProvider

    @classmethod
    def from_python(cls, username, options):
        return cls(username, **options)

    def __init__(self, username, group=None, groups=None, authorized_keys=None,
                 password=None, homedir=None, nohome=False, shell=None):
        self.username = username
        self.group = group
        self.groups = groups
        self.authorized_keys = authorized_keys
        self.password = password
        self.homedir = homedir
        self.nohome = nohome
        self.shell = shell

    def add(self):
        if not self.default_provider.exists(self.username):
            return self.default_provider.add(
                self.username, self.group, self.groups, self.authorized_keys,
                self.password, self.homedir, self.nohome, self.shell)
        return False

    def remove(self):
        if self.default_provider.exists(self.username):
            return self.default_provider.remove(self.username)
        return False


class Group(object):
    root_key = 'groups'
    uses_key = False
    default_provider = GroupProvider

    @classmethod
    def from_python(cls, options):
        return cls(options)

    def __init__(self, name):
        self.name = name

    def add(self):
        if not self.default_provider.exists(self.name):
            return self.default_provider.add(self.name)
        return False

    def remove(self):
        if self.default_provider.exists(self.name):
            return self.default_provider.remove(self.name)
        return False
